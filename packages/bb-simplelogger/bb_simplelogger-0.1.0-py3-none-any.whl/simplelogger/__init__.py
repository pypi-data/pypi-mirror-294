import os, sys, re, logging, atexit, io
from tempfile import NamedTemporaryFile as tmpfile
from pathlib import Path
from datetime import datetime as DT
from traceback import format_exception
from inspect import currentframe
from functools import wraps

global FILE_HANDLERS, LOG_RECORDS, WRITE_AT_EXIT, LOG_DATE_FORMAT, DEFAULT_HTML_THEME
from .constants import FILE_HANDLERS, LOG_RECORDS, WRITE_AT_EXIT, LOG_DATE_FORMAT, DEFAULT_HTML_THEME

def iter_escapes(s):
    esc = re.compile(r'\x1b\[[0-9]*?[A-G]{1}|\x1b\[[0-9;]+[Hf]{1}|\x1b\[[Hsu]{1}|\x1b\[[0-2]?[JK]{1}|\x1b[M78]{1}|\x1b\[[0-9;]+?m')
    for m in esc.finditer(s):
        yield m

def rmEsc(s):
    esc = re.compile(r'\x1b\[[0-9]*?[A-G]{1}|\x1b\[[0-9;]+[Hf]{1}|\x1b\[[Hsu]{1}|\x1b\[[0-2]?[JK]{1}|\x1b[M78]{1}|\x1b\[[0-9;]+?m')
    return esc.sub( '', s )

def _terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 160

def log_to_html( path, *, title, to_pdf, theme, overwrite ):
    import simplelogger.html as Html
    log = SimpleLogger('SimpleLogger')

    try:
        data = LOG_RECORDS.getvalue().strip()
        assert data
    except Exception as E:
        log.error( E, "Couldn't write html/pdf file - no logfile data found" )
        return

    if not path.parent.is_dir():
        log.error(f"Couldn't write html/pdf file - '{path.parent}' doesn't exist!")

    if to_pdf:
        path = path.parent.joinpath( f"{path.stem}.pdf" )

    if not title:
        title = 'Log: '
    else:
        title = f"{title.rstrip(':')}: "
    title += DT.now().strftime( '%Y-%d-%d %I:%M%P' )

    t = Html.HtmlThemes()
    if theme not in t:
        log.error(f"Invalid theme '{theme}'")
        theme = DEFAULT_HTML_THEME

    if to_pdf:
        html = Html.AnsiHtml( data, theme = theme, title = title )
        html.save( path, to_pdf = True, overwrite = overwrite )

    else:
        html = Html.AnsiHtml( data, no_page_limits = True, theme = theme, title = title )
        html.save( path, overwrite = overwrite )

class FileHandler( logging.FileHandler ):
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.setLevel( logging.DEBUG )

    def format(self, record):
        rec = rmEsc( super().format( record ))
        if len( rec.split('\n') ) > 1:
            line = rec.split('\n')[-1]
            if re.match( r'^\[[0-9:\-_ /]+$', line.strip() ):
                line = f" {line.strip()}"
                _rec =  rec.split('\n')[:-1]
                space = max([ len(i) for i in _rec ]) - len(_rec[-1])
                rec = '\n'.join( _rec ) + f"{'':{space}}{line}"
        return rec

class SimpleLogger( logging.getLoggerClass() ):
    """
    Custom Logger
    """
    _levels_ = { '1': 'debug',
                 '2': 'info',
                 '3': 'warning',
                 '4': 'error',
                 '5': 'critical' }

    _level_names_ = dict([( v, k ) for k, v in _levels_.items() ])
    name = ''
    level = 3

    def __init__( self, name = '', level = 0, *,
                  logfile = '',
                  html_theme = 'plain_builtin',
                  terminal_output = True,
                  overwrite = False,
                  logfile_level = 1,
                  logfile_title = "",
                  to_html = '',
                  to_pdf = False,
                  date_fmt = '',
                  ):
        """
        All options and keyword arguments are optional

        Arguments:
            'name':  str - name given to logger
            'level': int [1-5] - terminal output logging level - default is 3

        Keyword Arguments:
            'date_fmt':        str ['%H:%M:%S'] - date format string
            'html_theme':      str ['plain'] - html theme to use when writing html or pdf
                                - see SimpleLogger.view_html_themes() to print examples
            'terminal_output': bool [True] - whether or not to output logs to terminal
            'logfile':         str - plaintext log file to write in realtime
            'overwrite':       bool [False] - overwrite logfile at initial start of program if existing
            'logfile_level':   int [1-4] - limit logs at or above level given - default is 1
            'logfile_title':   str - prepend text to logfile (shows date and time only by default)
                                - also applies to html/pdf if used
            'to_html':         str [path] - write logs to an html file at exit of program
            'to_pdf':          bool - use with 'to_html' to instead save a pdf
                                - REQUIREMENT: chrome or chromium and bash in system path
        """
        global LOG_RECORDS, LOG_DATE_FORMAT, WRITE_AT_EXIT, DEFAULT_HTML_THEME
        super().__init__( name, level = logging.DEBUG )

        self._records = LOG_RECORDS
        self.root.setLevel(logging.DEBUG)
        self.propagate = False

        if terminal_output:
            self.addHandler( logging.StreamHandler() )

        if date_fmt:
            self.date_fmt = date_fmt
        else:
            self.date_fmt = LOG_DATE_FORMAT

        try:
            assert 'BBLOGGER_VERBOSITY' in os.environ
            self.setLevel( os.environ['BBLOGGER_VERBOSITY'] )
        except AssertionError:
            pass
        except ValueError:
            sys.stderr.write(f"\x1b[1;31m  [ERROR]\x1b[0;2;37;3m Invalid value for 'BBLOGGER_VERBOSITY' - '{os.environ['BBLOGGER_VERBOSITY']}'\x1b[0m")
            sys.stderr.write(f"\x1b[1;31m  [ERROR]\x1b[0;2;37;3m Logging level '{self.levelname()}' unchanged\x1b[0m")
        except Exception as E:
            sys.stderr.write(f"\x1b[1;31m  [ERROR]\x1b[0;2;37;3m {E}\x1b[0m")
            sys.stderr.write(f"\x1b[1;31m  [ERROR]\x1b[0;2;37;3m Logging level '{self.levelname()}' unchanged\x1b[0m")

        if level:
            self.setLevel( level )

        if logfile:
            self.addFileHandler( logfile, overwrite = bool(overwrite), level = int(logfile_level), log_title = str(logfile_title) )

        if level:
            self.setLevel(level)
        else:
            self.setLevel(3)

        if to_html:
            if WRITE_AT_EXIT:
                self.warning(f"Can only enable writing on exit one time in program!")
            else:
                WRITE_AT_EXIT = True
                p = Path(to_html).absolute()
                path = p.parent.joinpath( f"{p.stem}.html" )
                self.info(f"Writing on exit to '{path}'")
                atexit.register( log_to_html, path,
                                 to_pdf = bool(to_pdf),
                                 overwrite = overwrite,
                                 title = str(logfile_title),
                                 theme = html_theme )

    def __call__( self, *args ):
        LEVEL = None
        MESSAGES = []
        EXCEPTION = None
        msg = ''
        levels = ( 'debug', 'info', 'warning', 'error', 'critical' )

        args = list(args)
        while args:
            arg = args.pop(0)
            if not LEVEL and ( isinstance( arg, int ) or ( isinstance( arg, str ) and arg in levels )):
                if arg not in range(1,6):
                    raise ValueError(f"Invalid level '{arg}' - must be 1 - 5")
                LEVEL = levels[arg]

            elif isinstance( arg, Exception ):
                if EXCEPTION:
                    raise SyntaxError("Only one exception can be logged at a time")
                EXCEPTION = arg

            elif isinstance( arg, str ):
                MESSAGES.append(arg)

            else:
                raise SyntaxError(f"Invalid argument for logger '{arg}'")

        if not LEVEL:
            if EXCEPTION:
                LEVEL = 'error'
            else:
                LEVEL = 'debug'

        if MESSAGES:
            msg = f"\n{'':{len(LEVEL) + 5}}".join( MESSAGES )

        return getattr( self, LEVEL )( *filter( None, [ msg, EXCEPTION ]))

    def addFileHandler( self, path = None, *, level = 1, overwrite = False, log_title = "" ):
        global FILE_HANDLERS
        hdlr = self.getFileHandler()
        if hdlr:
            return

        elif not FILE_HANDLERS and ( not path or isinstance( path, int )):
            raise ValueError(f"No files in global file handlers")

        elif not path:
            self.addHandler( FILE_HANDLERS[0][1] )
            return

        elif isinstance( path, int ):
            if path >= len(FILE_HANDLERS):
                raise IndexError(f"Invalid index '{path}' for file handler")
            self.addHandler( FILE_HANDLERS[path][1] )
            return

        file = Path(path).absolute()
        if not file.parent.is_dir():
            raise ValueError(f"Directory '{file.parent}' doesn't exist!")
        elif file.is_dir():
            raise ValueError(f"File '{file}' is already a directory!")

        if log_title:
            log_title += ' - '

        filehandlers = dict(FILE_HANDLERS)
        if file in filehandlers:
            fh = filehandlers[file]

        else:
            width = _terminal_width()
            title = '\n'.join([ f"{'':-<{width}}",
                                f"# {log_title}{DT.now().strftime( '%Y-%m-%d %H:%M:%S' )}",
                                f"{'':-<{width}}", '', '' ])

            if not file.exists() or ( file.exists() and overwrite ):
                with open( file, 'w' ) as f:
                    f.write( title )
            else:
                with open( file, 'a' ) as f:
                    f.write( '\n' + title )

            fh = FileHandler( str(file) )
            fh.setLevel( self._get_level(level) )
            FILE_HANDLERS += (( file, fh ), )

        self.addHandler(fh)

    def _fmt_exception( self, E ):
        ecol = '\x1b[0;38;2;160;160;160;48;2;26;26;26m'
        hlcol = '\x1b[0;38;2;211;57;40;48;2;26;26;26;1m'
        lcol = '\x1b[0;38;2;102;255;102;48;2;26;26;26;1m'
        tbcol = '\x1b[0;38;2;163;71;41;48;2;26;26;26;3m'
        fncol = '\x1b[0;38;2;6;138;172;48;2;26;26;26;1m'
        fcol = '\x1b[0;38;2;46;180;222;48;2;26;26;26;3m'
        # txt = '\x1b[38;2;155;49;62;3;1m'
        w = _terminal_width() - 4
        elines = [ '', *''.join(format_exception(E)).strip().split('\n')[:-1], '' ]
        maxw = max([ len(i) + 4 for i in elines ])
        if maxw <= w:
            indent = ''.join([ ' ' for i in range(int( (w - maxw) / 2 )) ])
            lines = [ f"{indent}{ecol}  {i:{maxw - 2}}\x1b[0m" for i in elines ]

        else:
            lines = []
            for line in elines:
                if len(line) <= w - 2:
                    lines.append( f"  {ecol}  {line:{w-2}}\x1b[0m" )
                    continue

                words = line.split(' ')
                _line = ''
                while words:
                    if not _line:
                        _line = f"  {words.pop(0)}"
                        continue

                    word = f" {words.pop(0)}"
                    if len(_line) + len(word) > w:
                        lines.append( f"  {ecol}{_line:{w}}\x1b[0m" )
                        _line = f"       {word}"
                    else:
                        _line += word

                if _line:
                    lines.append( f"  {ecol}{_line:{w}}\x1b[0m" )

        if lines:
            exc_lines = '\n'.join(lines)
            for M, C in [ ( r'\^+', hlcol ), ( r'line [0-9]+\b', lcol ),
                          ( r'Traceback \(.+?:', tbcol ), ( r'(?<= in )[a-zA-Z0-9_]+\b', fncol ),
                          ( r'(?<=File ")[^"]+', fcol )]:
                matches = list(re.finditer( M, exc_lines ))
                for m in sorted( matches, key = lambda x: x.span()[0], reverse = True ):
                    s, e = m.span()
                    exc_lines = exc_lines[:s] + f"{C}{m.group()}{ecol}" + exc_lines[e:]

            exc = f"\x1b[38;2;106;14;14m Exception raised\x1b[0;38;2;240;240;253;1m <<\x1b[0m\n\n" + exc_lines + f"\n\n\x1b[0;38;2;211;57;40;1m     {type(E).__name__}:"
        else:
            exc = f"\x1b[38;2;106;14;14m Exception raised\x1b[0;38;2;240;240;253;1m <<\n\x1b[0;38;2;211;57;40;1m     {type(E).__name__}:"

        return exc

    def _print_log(func):
        import re
        @wraps(func)
        def _wrap( self, s, exc = None ):
            level, col, levelname = func(self)

            if isinstance( s, Exception ):
                _exc = exc
                exc = s
                s = _exc
                del _exc

            tb = currentframe().f_back
            lineno = f"\x1b[0;38;2;240;240;253;1m<\x1b[0;38;2;166;243;224;1m{tb.f_lineno}\x1b[0;38;2;240;240;253;1m>"
            if self.name:
                name = f"\x1b[0;38;2;221;232;228;1m{self.name}\x1b[0;38;2;240;240;253;1m."
            else:
                try:
                    name = f"\x1b[0;38;2;221;232;228;1m{Path( tb.f_code.co_filename.replace('.py','') ).name}\x1b[0;38;2;240;240;253;1m."
                except:
                    name = ''

            exc_str = ''
            if isinstance( exc, Exception ):
                exception = self._fmt_exception( exc )
                if str(exc):
                    exc_str = str(exc)
                else:
                    exc_str = str(s)
            elif isinstance( s, Exception ):
                exception = self._fmt_exception( s )
                exc_str = str(s)
            else:
                exception = ''

            txt = '\x1b[0;38;2;105;138;133;3m'
            pre_msg = f" {lineno}{col} [{levelname}] {name}{col}{tb.f_code.co_qualname}\x1b[0;38;2;240;240;253;1m >>"
            msg = f"{pre_msg}{exception}{txt} "
            if exc_str:
                if s and exc_str != str(s):
                    msg += f"{exc_str}\n{col}        [{levelname}]:{txt} {s}"
                else:
                    msg += f"{exc_str}"

            else:
                msg += s

            time = f" [{DT.now().strftime( self.date_fmt )}]"
            self._records.write(f"{col}{time}{msg}\x1b[0m\n\n")

            clean = rmEsc( msg.split('\n')[-1] )
            width = _terminal_width() - 1
            tlen = len(time)
            mlen = len(clean)

            if tlen + mlen > width:
                msg += f"\n{'':{width-tlen}}\x1b[0;38;2;166;243;224m{time}\x1b[0m"
            else:
                msg += f"{'':{width - (tlen + mlen)}}\x1b[0;38;2;166;243;224m{time}\x1b[0m"

            return self._log( level, msg, () )

        return _wrap

    @_print_log
    def debugging(self): return logging.DEBUG, '\x1b[0;38;2;195;195;195;1m', "DEBUG"
    @_print_log
    def debug(self): return logging.DEBUG, '\x1b[0;38;2;195;195;195;1m', "DEBUG"
    @_print_log
    def info(self): return logging.INFO, '\x1b[0;38;2;100;185;222;1m', "INFO"
    @_print_log
    def warning(self): return logging.WARNING, '\x1b[0;38;2;179;206;83;1m', "WARNING"
    @_print_log
    def warn(self): return logging.WARNING, '\x1b[0;38;2;179;206;83;1m', "WARNING"
    @_print_log
    def error(self): return logging.ERROR, '\x1b[0;38;2;211;57;40;1m', "ERROR"
    @_print_log
    def err(self): return logging.ERROR, '\x1b[0;38;2;211;57;40;1m', "ERROR"
    @_print_log
    def critical(self): return logging.CRITICAL, '\x1b[0;38;2;241;77;60;1m', "CRITICAL"

    def _get_level( self, level ):
        for i, (k, v) in enumerate(list(self._levels_.items())):
            if level in [ i, k, v ]:
                return i * 10
        raise ValueError(f"Invalid logging level '{level}'")

    def setLevel( self, level ):
        level = self._get_level(level)

        hdlr = self.getStreamHandler()
        if hdlr:
            hdlr.setLevel(level)

    def listFileHandlers(self):
        return [ i[1] for i in FILE_HANDLERS ]

    def levelname(self):
        return dict( self._levels_ )[ str( self.level ) ]

    def getStreamHandler(self):
        try:
            return list(filter( lambda x: isinstance( x, logging.StreamHandler ), self.handlers ))[0]
        except:
            return None

    def getFileHandler(self):
        try:
            return list(filter( lambda x: isinstance( x, FileHandler ), self.handlers ))[0]
        except:
            return None

    def removeFileHandler(self):
        hdlr = self.getFileHandler()
        if hdlr:
            self.removeHandler(hdlr)

    @classmethod
    def view_html_themes(cls):
        from .html import HtmlThemes
        t = HtmlThemes()
        t.view_examples()
