import re, os, sys, io, json
from functools import wraps
from shutil import move as MV
from types import FunctionType
from threading import Thread, Lock, Event
from tempfile import NamedTemporaryFile as tmpfile
from importlib.resources import files as _src
from pathlib import Path
import simplelogger
log = simplelogger.SimpleLogger(__name__)

from .pdf import toPDF, unique
from . import _data

global DEFAULT_HTML_THEME
from .constants import DEFAULT_HTML_THEME

void_elements = ( '<area', '<base', '<br', '<col', '<embed',
                  '<hr', '<img', '<input', '<link', '<meta',
                  '<param', '<source', '<track', '<wbr', '<!doctype', '<!DOCTYPE' )
inline_elements = ( '<b>', '</i>', '<u>', '</sup>', '<sub>', '</strong>', '<em>',   # '</span', '<pre',
                    '</b>', '<i>', '</u>', '<sup>', '</sub>', '<strong>', '</em>' ) # '<span', '</pre' )

def ansi_to_rgb( ansi ):
    _re = re.compile( r'\b(48|38);2(;(' + '|'.join([str(i) for i in reversed(range(256))]) + r')){3}' )
    try:
        return tuple( int(n) for n in _re.search( str(ansi) ).group().split(';')[-3:] )
    except:
        raise ValueError(f"Color escape not found in string {repr(ansi)}")

def fix_special_characters(s):
    chars = [( '<', '&lt;' ),
             ( '>', '&gt;' ),
             ( '\n', '<br>' )]

    for rep in chars:
        s = s.replace( *rep )
    return s

class HtmlTheme(dict):
    _builtin_ = True
    _defaults = { 'fg_color': 'rgb(42, 42, 42)', 'bg_color': 'rgb(255, 255, 255)',
                  'border_color': 'transparent', 'border_style': 'hidden', 'border_size': '0px',
                  'header_footer_color': 'transparent', 'header_footer_style': 'hidden', 'header_footer_size': '0px' }
    _keys = tuple( _defaults )
    _styles = [( 'none',    'Default value. Specifies no border'                                          ),
               ( 'hidden',  'The same as "none", except in border conflict resolution for table elements' ),
               ( 'dashed',  'Specifies a dashed border'                                                   ),
               ( 'dotted',  'Specifies a dotted border'                                                   ),
               ( 'solid',   'Specifies a solid border'                                                    ),
               ( 'double',  'Specifies a double border'                                                   ),
               ( 'groove',  'Specifies a 3D grooved border. The effect depends on the border-color value' ),
               ( 'ridge',   'Specifies a 3D ridged border. The effect depends on the border-color value'  ),
               ( 'inset',   'Specifies a 3D inset border. The effect depends on the border-color value'   ),
               ( 'outset',  'Specifies a 3D outset border. The effect depends on the border-color value'  )]

    def __init__( self, *, name, fg_color, bg_color, user = False, **kwargs ):
        dict.__init__(self)

        self.name = name.title()
        if user:
            self._builtin_ = False

        kwargs = { 'fg_color': fg_color, 'bg_color': bg_color, **kwargs }
        D = {}

        rgb_match = '(' + '|'.join([ str(i) for i in range(256) ]) + ')'
        for key in self._keys:
            KEY = key.upper()
            if key not in kwargs:
                log.debug(f"Using default theme value for '{key}'")
                D[KEY] = self._defaults[key]
                continue

            item = kwargs[key]
            try:
                if key.endswith('color'):
                    if not item or item == 'transparent':
                        D[KEY] = 'transparent'
                        continue

                    elif isinstance( item, str ):
                        if re.match( r'^#?[a-f0-9]{6}$', item, re.IGNORECASE ):
                            rgb = tuple( int( item.lstrip('#')[i:i+2], 16 ) for i in [0, 2, 4])
                        elif re.match( fr'^rgb\( *{rgb_match} *, *{rgb_match} *, *{rgb_match} *\)$', item, re.IGNORECASE ):
                            rgb = tuple( int(i) for i in item.split('(')[1][:-1].split(',') )
                        elif re.match( fr'^\( *{rgb_match} *, *{rgb_match} *, *{rgb_match} *\)$', item, re.IGNORECASE ):
                            rgb = tuple( int(i) for i in item.split('(')[1][:-1].split(',') )
                        else:
                            raise ValueError

                    elif isinstance( item, tuple ):
                        assert len(item) == 3 and all( i in range(256) for i in item )
                        rgb = item

                    D[KEY] = f"rgb{rgb}"

                elif key.endswith('size'):
                    if not item:
                        n = 0
                    elif isinstance( item, str ) and re.match( r'^[0-9]+px$', item, re.IGNORECASE ):
                        n = int(item[:-2])
                    else:
                        n = int(item)
                    D[KEY] = f"{n}px"

                elif key.endswith('style'):
                    assert item.lower() in [ i[0] for i in self._styles ]
                    D[KEY] = item.lower()

            except:
                raise ValueError(f"Invalid value '{item}' for key '{key}'")

        if D['FG_COLOR'] == 'transparent':
            log.warning(f"Can't have a transparent foreground color")
            comp = int( sum([255,255,255]) / 2 )
            if sum( self.bg() ) > comp:
                col = 'rgb(0, 0, 0)'
            else:
                col = 'rgb(255, 255, 255)'
            D['FG_COLOR'] = col

        self.update(D)

    def __repr__(self):
        return f"HtmlTheme(< {self.name} >)"

    def view(self):
        try:
            _bdr = ';38;2;' + ';'.join([ str(i) for i in self.border() ])
        except:
            _bdr = ''

        try:
            _hf = ';38;2;' + ';'.join([ str(i) for i in self.header_footer() ])
        except:
            _hf = ''

        try:
            _bg = ';48;2;' + ';'.join([ str(i) for i in self.bg() ])
        except:
            _bg = ''
        try:
            _fg = ';38;2;' + ';'.join([ str(i) for i in self.fg() ])
        except:
            _fg = ''

        b = f"\x1b[0{_bg}{_bdr}m"
        t = f"\x1b[0{_bg}{_fg}m"
        _ = '\x1b[0m'

        b_style = self['BORDER_STYLE']
        b_size = int(self['BORDER_SIZE'][:-2])
        hf_style = self['HEADER_FOOTER_STYLE']
        hf_size = int(self['HEADER_FOOTER_SIZE'][:-2])

        def _index( style, size ):
            if style in ['none', 'hidden', 'inset', 'outset', 'double', 'ridge', 'groove' ]:
                return 0 if style in ['none', 'hidden'] else 7
            _n = { 'solid': 1, 'dashed': 3, 'dotted': 5 }[style]
            if size >= 4:
                return _n + 1
            return _n

        n = _index( b_style, b_size )
        hf = _index( hf_style, hf_size )

        title = 'Builtin Theme:' if self._builtin_ else 'User Theme:'

        #     None   light     heavy    Ldashed   Hdashed   Ldotted   Hdotted  in/outset
        H  = ( ' ', '\u2500', '\u2501', '\u254C', '\u254D', '\u2504', '\u2505', '\u2550' )
        V  = ( ' ', '\u2502', '\u2503', '\u2506', '\u2507', '\u250A', '\u250B', '\u2551' )
        tl = ( ' ', '\u250C', '\u250F', '\u250C', '\u250F', '\u250C', '\u250F', '\u2554' )
        tr = ( ' ', '\u2510', '\u2513', '\u2510', '\u2513', '\u2510', '\u2513', '\u2557' )
        bl = ( ' ', '\u2514', '\u2517', '\u2514', '\u2517', '\u2514', '\u2517', '\u255A' )
        br = ( ' ', '\u2518', '\u251B', '\u2518', '\u251B', '\u2518', '\u251B', '\u255D' )

             # '', f"\x1b[38;2;240;240;250;1m    {title} {t} {self.name} {_}",
        R = [ '',
              f"        {b}{'':44}{_}",
              f"        {t}{f'{title} \x1b[4;1m{self.name}\x1b[24m':^55}{_}",
              f"        {b} {'':{H[hf]}<42} {_}",
              f"        {b}  {tl[n]}{'':{H[n]}<38}{tr[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{t}{'Hello World!':^38}{b}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {V[n]}{'':38}{V[n]}  {_}",
              f"        {b}  {bl[n]}{'':{H[n]}<38}{br[n]}  {_}",
              f"        {b} {'':{H[hf]}<42} {_}",
              f"        {b}{'':44}{_}", '' ]

        return '\n'.join(R)

    def __to_rgb_tuple(func):
        @wraps(func)
        def _wrap(self):
            val = func(self)
            if val.startswith('rgb('):
                return tuple( int(i.strip()) for i in val[4:-1].split(',') )
            return None
        return _wrap

    @__to_rgb_tuple
    def fg(self): return self['FG_COLOR']
    @__to_rgb_tuple
    def bg(self): return self['BG_COLOR']
    @__to_rgb_tuple
    def border(self): return self['BORDER_COLOR']
    @__to_rgb_tuple
    def header_footer(self): return self['HEADER_FOOTER_COLOR']

class HtmlThemes(dict):
    usr_dir = Path( os.path.expanduser('~') ).joinpath( '.config', 'beebe_apps', 'texttools' )
    user_themes = {}
    app_themes = {}

    def __init__( self, *args, **kwargs ):
        dict.__init__(self)
        user = self._load_user()
        app = self._load_app()
        self.update( **user, **app )

    def __repr__(self):
        return f"HtmlThemes(< {len(self)} themes >)"

    def __contains__( self, name ):
        return str(name).lower() in list(self.keys())

    def __setitem__( self, name, value ):
        log.error(f"Add new themes by editing 'html-themes.json' in '{self.usr_dir}'")
        return

    def __getitem__( self, key ):
        if key.lower() == 'default':
            return self.default()

        try:
            return super().__getitem__( str(key).lower() )
        except Exception as E:
            log.error( E, f"Invalid theme name '{key}'" )
            raise

    def default(self):
        global DEFAULT_HTML_THEME
        if DEFAULT_HTML_THEME not in list(self):
            DEFAULT_HTML_THEME = 'plain'

        return self[ DEFAULT_HTML_THEME ]

    def get_examples(self):
        R = []
        for key in self.keys():
            R.append( self[key].view() )

        return '\n\n'.join(R)

    def _load_app(self):
        app = {}
        file = _src(_data).joinpath( 'html-themes.json' )

        try:
            with open( file, 'r' ) as f:
                data = json.load(f)
            for theme in data:
                app[ theme['name'].lower() ] = HtmlTheme( **theme )

        except Exception as E:
            raise RuntimeError( E, "Unable to load application themes" )

        return app

    def _load_user(self):
        user = {}
        file = self.usr_dir.joinpath( 'html-themes.json' )

        try:
            with open( file, 'r' ) as f:
                data = json.load(f)

            for theme in data:
                user[ theme['name'].lower() ] = HtmlTheme( **theme, user = True )
            user['plain'] = HtmlTheme( **self._plain(), user = True )

        except Exception as E:
            if file.exists():
                backup = unique( file.joinpath( f"~{file.name}" ))
                log.error( E, f"Theme file '{file}' could not be read, backing up to '{backup}'" )
                MV( file, backup )

            self._save_themes()
            return self._load_user()

        return user

    def _plain(self):
        return { "name": "Plain",
                 "fg_color": "#10100f",
                 "bg_color": "#ffffff",
                 "border_color": "transparent",
                 "border_style": "hidden",
                 "border_size": "0px",
                 "header_footer_color": "transparent",
                 "header_footer_style": "hidden",
                 "header_footer_size": "0px" }

    def _save_themes(self):
        os.makedirs( self.usr_dir, exist_ok = True )
        usr_file = self.usr_dir.joinpath( 'html-themes.json' )
        themes = list(filter( lambda x: not x._builtin_, self.values() ))

        if not themes:
            super().__setitem__( 'plain', HtmlTheme( **self._plain() ))
            themes = [ self['plain'] ]

        data = []
        for theme in themes:
            data.append({ 'name': theme.name })
            for key, val in theme.items():
                if val.startswith('rgb('):
                    data[-1][ key.lower() ] = '#%02x%02x%02x'%tuple( int(i.strip()) for i in val[4:-1].split(',') )
                else:
                    data[-1][ key.lower() ] = val

        with open( usr_file, 'w' ) as f:
            json.dump( sorted( data, key = lambda x: x['name'] ), f, indent = '    ' )

        log.info(f"Theme file saved to '{usr_file}'")

    def view_example( self, theme ):
        t = self[theme]
        print( t.view() )

    def view_examples(self):
        R = [ '', f"  \x1b[38;2;240;240;250;1;4mTheme Examples:\x1b[0;38;2;9;197;246;3m  {len(self)} themes\x1b[0m",
              *[ self[key].view() for key in self.keys() ]]

        print( '\n'.join(R) )

class AnsiHtml:
    """
    Create HTML data from a string containing ansi escapes
        - ignores and removes escapes that don't effect color or style
    """

    __tmp__ = ''
    _lock = Lock()
    _max_threads = os.cpu_count()
    _allow_blink = False
    _template = _src(_data).joinpath( 'html_template.html' )
    _style_codes = { '1': ( 'style', 'font-weight', 'bold' ),
                     '2': ( 'style', 'opacity', '0.6' ),
                     '3': ( 'style', 'font-style', 'italic' ),
                     '4': ( 'style', 'text-decoration', 'underline' ),
                     '5': ( 'id', 'blink_effect' ),
                     '7': ( 'style', 'color', '%(LAST_BG)s', 'background', '%(LAST_FG)s' ),
                     '8': ( 'style', 'visibility', 'hidden' ),
                     '9': ( 'style', 'text-decoration', 'line-through' ),
                     '21': ( 'style', 'font-weight', 'normal' ),
                     '22': ( 'style', 'opacity', '1.0' ),
                     '23': ( 'style', 'font-style', 'none' ),
                     '24': ( 'style', 'text-decoration', 'none' ),
                     '25': ( 'id', 'no_blink' ),
                     '27': ( 'style', 'color', '%(FG_COLOR)s', 'background', '%(BG_COLOR)s' ),
                     '28': ( 'style', 'visibility', 'show' ),
                     '29': ( 'style', 'text-decoration', 'none' ) }

    _8bit_codes = { '30'  : { 'color': 'rgb(0,0,0)'      },     #  Black       - #000000
                    '1;30': { 'color': 'rgb(104,104,104)'},     #  Gray        - #686868
                    '2;30': { 'color': 'rgb(24,24,24)'   },     #  Dark Gray   - #181818
                    '31'  : { 'color': 'rgb(178,24,24)'  },     #  Red         - #B21818
                    '1;31': { 'color': 'rgb(255,84,84)'  },     #  Light Red   - #FF5454
                    '2;31': { 'color': 'rgb(101,0,0)'    },     #  Dark Red    - #650000
                    '32'  : { 'color': 'rgb(24,178,24)'  },     #  Green       - #18B218
                    '1;32': { 'color': 'rgb(84,255,84)'  },     #  Light Green - #54FF54
                    '2;32': { 'color': 'rgb(0,101,0)'    },     #  Dark Green  - #006500
                    '33'  : { 'color': 'rgb(178,104,24)' },     #  Orange      - #B26818
                    '1;33': { 'color': 'rgb(255,255,84)' },     #  Yellow      - #FFFF54
                    '2;33': { 'color': 'rgb(101,94,0)'   },     #  Gold        - #655E00
                    '34'  : { 'color': 'rgb(24,24,178)'  },     #  Blue        - #1818B2
                    '1;34': { 'color': 'rgb(84,84,255)'  },     #  Light Blue  - #5454FF
                    '2;34': { 'color': 'rgb(0,0,101)'    },     #  Dark Blue   - #000065
                    '35'  : { 'color': 'rgb(178,24,178)' },     #  Purple      - #B218B2
                    '1;35': { 'color': 'rgb(255,84,255)' },     #  Pink        - #FF54FF
                    '2;35': { 'color': 'rgb(101,0,101)'  },     #  Dark Purple - #650065
                    '36'  : { 'color': 'rgb(24,178,178)' },     #  Cyan        - #18B2B2
                    '1;36': { 'color': 'rgb(84,255,255)' },     #  Light Cyan  - #54FFFF
                    '2;36': { 'color': 'rgb(0,101,101)'  },     #  Dark Cyan   - #006565
                    '37'  : { 'color': 'rgb(178,178,178)'},     #  Light Gray  - #B2B2B2
                    '1;37': { 'color': 'rgb(255,255,255)'},     #  White       - #FFFFFF
                    '2;37': { 'color': 'rgb(101,101,101)'} }    #  Silver      - #656565

    for key in list(_8bit_codes):
        _8bit_codes[ key.replace('3','4',1) ] = { 'background': _8bit_codes[key]['color'] }

    _data_dict = { 'DATA': '',
                   'DATA_PATH': str(_src(_data).joinpath('blah').parent),
                   'PAGE_WIDTH': '8.5in',
                   'PAGE_HEIGHT': '11in',
                   'PAGE_ZOOM': '100%',
                   'TITLE': '&nbsp;',
                   'PAGE_SIZE': 'default',
                   }

    _esc_re = re.compile(r'\x1b(\[[0-9]*?[A-G]{1}|\[[0-9;]+[Hf]{1}|\[[Hsu]{1}|\[[0-2]?[JK]{1}|[M78]{1}|\[[0-9;]++m)')
    # _esc_re = re.compile(r'\x1b\[[0-9]*?[A-G]{1}|\x1b\[[0-9;]+[Hf]{1}|\x1b\[[Hsu]{1}|\x1b\[[0-2]?[JK]{1}|\x1b[M78]{1}|\x1b\[[0-9;]+?m')
    _color_re = re.compile( r'\x1b\[[0-9]+(;[0-9]+)*m' )
    _rgb_re = re.compile( r';?\b(48|38);2(;(' + '|'.join([str(i) for i in reversed(range(256))]) + r')){3}' )
    _8bit_re = re.compile( r'\b;?(1|2|30|31|32|33|34|35|36|37|40|41|42|43|44|45|46|47|48){1}\b' )
    _style_re = re.compile( r'\b;?[1-57-9]{1}\b' )

    Theme = HtmlThemes()
    string = ''
    theme = Theme['default']
    escapes = ()
    saved = None
    block_separator = '\n\n'
    columns = 0
    listing = False

    def __init__( self, string, *, page_print_size = '', scale = None, no_page_limits = False, theme = None, title = '', blinking_text = False, block_sep = None, columns = 0 ):
        if theme:
            if isinstance( theme, str ):
                theme = self.Theme[theme]
            elif not isinstance( theme, HtmlTheme ):
                raise TypeError(f"Invalid type '{type(theme).__name__}' for theme, expected HtmlTheme")
            self.theme = theme
            fg = theme['FG_COLOR']
            bg = theme['BG_COLOR']
            self._latest = { 'LAST_FG': fg, 'LAST_BG': bg, 'BG_COLOR': bg, 'FG_COLOR': fg }

        self.string = str(string)
        self._data_dict = { **self._data_dict, **self.theme }
        if title:
            title = self.parse_string( str(title) )
            if ':' in title:
                main, sub = title.split(':',1)
                title = f'{main}:<span style="font-size: 11pt;">{sub}</span>'

            self._data_dict['TITLE'] = title

        if block_sep != None:
            self.block_separator = str(block_sep)

        if columns:
            self.columns = abs(int(columns))

        if no_page_limits:
            self._data_dict['PAGE_WIDTH'] = '100%'
            self._data_dict['PAGE_HEIGHT'] = '100%'

        if scale:
            if isinstance( scale, str ) and re.match( r'^[0-9]+%$', scale ):
                pass
            elif isinstance( scale, int|float ):
                if scale % 1 != 0:
                    scale = f"{round( scale * 100 )}%"
                else:
                    scale = f"{int(scale)}%"

            else:
                raise ValueError(f"Invalid scale '{scale}'")

            self._data_dict['PAGE_ZOOM'] = scale

        if page_print_size:
            self._data_dict['PAGE_SIZE'] = str(page_print_size).lower()

        self._parse_page(string)

    def __str__(self):
        return self['DATA']

    def __enter__(self):
        with open( self._template, 'r' ) as f:
            html = f.read()

        for k, v in self._data_dict.items():
            html = html.replace( f"%({k})s", v )

        self.__tmp__ = io.StringIO( html )
        self.__tmp__.seek(0)
        for attr in [ 'getvalue', 'read', 'readline', 'readlines', 'seek', 'tell' ]:
            setattr( self, attr, getattr( self.__tmp__, attr ))

        return self

    def __exit__( self, exc_type, exc_val, exc_tb ):
        for attr in [ 'getvalue', 'read', 'readline', 'readlines', 'seek', 'tell' ]:
            delattr( self, attr )

        self.__tmp__.close()
        self.__tmp__ = ''

    def __getitem__( self, key ):
        return self._data_dict[key]

    def iter( self, string ):
        for match in self._esc_re.finditer( string ):
            yield match

    def _reset(self):
        self._latest['LAST_FG'] = self.theme['FG_COLOR']
        self._latest['LAST_BG'] = self.theme['BG_COLOR']

    def _end_spans( self, string ):
        count = len( re.findall( r'<span.*?>', string )) - len( re.findall( r'</span>', string ))
        if count <= 0:
            if count < 0:
                log.error(f"Invalid span end count somewhere before character '{len(string)}'")
            return string
        return string + ''.join([ '</span>' for i in range(count) ])

    def _rgb( self, *, esc, **kwargs ):
        # log.debug(f"{esc = }")
        for match in sorted( list( self._rgb_re.finditer( esc )), key = lambda x: x.span()[0], reverse = True ):
            nums = [ int(i) for i in match.group().strip(';').split(';') ]
            s, e = match.span()
            esc = esc[:s] + esc[e:]
            kwargs['style'][ {38: 'color', 48: 'background'}[nums[0]] ] = f"rgb{tuple(nums[-3:])}"

        # log.debug(f"Removed {esc = }")
        return { 'esc': esc, **kwargs }

    def _8bit( self, *, esc, **kwargs ):
        # log.debug(f"{esc = }")
        highs = tuple( list( range(30,38) ) + list( range(40,48) ))
        lows = ( 1, 2 )

        matches = []
        def nums():
            return sorted([ int( i.group().strip(';') ) for i in matches ])

        while True:
            matches = []
            for match in sorted( list( self._8bit_re.finditer( esc )), key = lambda x: x.span()[0], reverse = True ):
                n = int( match.group().replace(';','') )
                if n in lows and any( i in nums() for i in lows ):
                    continue
                elif n in highs and any( i in nums() for i in highs ):
                    continue

                matches.append( match )

                if len(matches) == 2:
                    break

            if not any( i in highs for i in nums() ):
                break

            else:
                for m in matches:
                    s, e = m.span()
                    esc = esc[:s] + esc[e:]

                kwargs = { **kwargs, **self._8bit_codes[ ';'.join([ str(i) for i in nums() ]) ] }

        # log.debug(f"Removed 8-bit colors {esc = }")
        return { 'esc': esc, **kwargs }

    def _styles( self, *, esc, **kwargs ):
        # log.debug(f"{esc = }")
        for match in sorted( list( self._style_re.finditer( esc )), key = lambda x: x.span()[0], reverse = True ):
            s, e = match.span()
            esc = esc[:s] + esc[e:]

            data = self._style_codes[ match.group().strip(';') ]
            if len(data) == 5:
                kwargs[ data[0] ][ data[1] ] = data[2] % self._latest
                kwargs[ data[0] ][ data[3] ] = data[4] % self._latest
            elif len(data) == 3:
                if data[1] == 'text-decoration' and 'text-decoration' in kwargs['style'] and kwargs['style'][data[1]] != 'none':
                    kwargs[ data[0] ][ data[1] ] += f" {data[2]}"
                else:
                    kwargs[ data[0] ][ data[1] ] = data[2]
            elif self._allow_blink:
                kwargs[ data[0] ] = data[1]

        # log.debug(f"Removed styles {esc = }")
        return { 'esc': esc, **kwargs }

    def _esc_to_span( self, esc ):
        """
        Returns bool, str
            - bool: whether reset is in escape
            - str:  span string or '' if no styles found

            Escape code '5' (blink) adds a span with 'id: blink_effect' for

        """
        if not self._color_re.fullmatch( esc ):
            log.debug(f"Escape {repr(esc)} is not a color escape")
            return False, ''

        # log.debug(f"Escape = {repr(esc)}")

        esc = esc[2:-1]
        data = { 'esc': esc, 'style': {}, 'id': '' }
        span = ''

        for func in ( self._rgb, self._8bit, self._styles ):
            data = { **data, **func( **data )}

        esc = data['esc']
        reset = re.search( r'\b;?0\b', esc )
        if reset:
            s, e = reset.span()
            esc = esc[:s] + esc[e:]
            self._latest = { 'LAST_BG': self.theme['BG_COLOR'],
                             'LAST_FG': self.theme['FG_COLOR'] }

        if data['id']:
            span += f' id="{data['id']}"'

        if data['style']:
            style = data['style']
            if 'color' in style:
                self._latest['LAST_FG'] = style['color']
            if 'background' in style:
                self._latest['LAST_BG'] = style['background']

            style_data = 'style="' + '; '.join([ f"{k}: {v}" for k, v in style.items() ]) + ';"'
            span += f" {style_data}"

        esc = esc.strip(';')
        if esc:
            log.error(f"Couldn't parse all of escape code '{esc}'")

        # log.debug(f"Span = {repr(span)}")
        if span:
            span = f"<span{span}>"
        return bool(reset), span

    def _fix_unicodes( self, _str ):
        html, start, end = '', 0, len(_str)
        for match in re.finditer( r'\u[0-9a-fA-F]{4}', _str ):
            s, e = match.span()
            html += f"{_str[ start : s ]}&#x{match.group()[-4:]};"
            start = e

        return html + _str[ start : end ]

    def _get_current_spans( self, string ):
        span_starts = re.findall( r'<span.*?>', string )
        span_ends = re.findall( r'</span>', string )
        count = len(span_starts) - len(span_ends)
        if count > 0:
            return span_starts[-count:]
        return []

    def _parse_page( self, _str ):
        if self.block_separator:
            blocks = _str.split( self.block_separator )
        else:
            blocks = [ _str ]

        groups = []
        last_spans = []
        for block in blocks:
            string = fix_special_characters(block)

            hb = ''.join(last_spans)
            pre_index = len(hb)

            start = 0
            end = len(string)
            for match in self._esc_re.finditer( string ):
                s, e = match.span()
                add = string[ start : s ]
                log.debug(f"{add = }")
                hb += add
                start = e

                reset, span = self._esc_to_span( match.group() )
                if reset:
                    last_spans = []
                    hb = self._end_spans( hb )
                hb += span

            hb += string[ start : end ]

            if not hb[ pre_index : ]:
                continue

            last_spans += self._get_current_spans( hb )
            hb += ''.join([ '</span>' for i in range(len(last_spans)) ])
            # log.debug(f"Block after parsing:\n    {'<br>\n    '.join(hb.split('<br>'))}")
            groups.append( hb )

        if not groups:
            log.debug(f"Nothing to create html with!")
            return

        pre = '<div id="block" name="block_{blk_num}"><pre>'
        post = '</pre></div>'

        if self.listing:
            _in = '<ol>' if self.listing == 'ordered' else '<ul>'
            _out = '</ol>' if self.listing == 'ordered' else '</ul>'

            html = _in
            if self.columns:
                tbl_pre = '<li><table><tr>'
                html += tbl_pre
                n = 0
                while groups:
                    if n and n % self.columns == 0:
                        html += f'</tr></table></li>{tbl_pre}'

                    html += f'<td>{pre.format( blk_num = n )}{groups.pop(0)}{post}</td>'

                while n % self.columns != 0:
                    html += '<td></td>'
                html += '</tr></table></li>' + _out

            else:
                while groups:
                    html += f'<li>{groups.pop(0)}</li>'
                html += _out

        elif self.columns:
            col_width = round( ( 1 / self.columns ) * 100, 2 )
            html = '<table style="width: 100%; align-content: center; margin-left: auto; margin-right: auto;"><tr>'
            n = 0
            while groups:
                if n and n % self.columns == 0:
                    html += '</tr><tr>'
                html += f'<td style="width: {col_width}%; align-content: center;">{pre.format( blk_num = n )}{groups.pop(0)}{post}</td>'
                n += 1

            while n % self.columns != 0:
                html += '<td></td>'
                n += 1

            html += '</tr></table>'

        else:
            html = ''.join([ f"{pre.format( blk_num = i )}{G}{post}" for i, G in enumerate(groups) ])

        self._reset()
        self._data_dict['DATA'] = formatHtml( html, initial_indent = 12 ).strip()

    def parse_string( self, string ):
        string = fix_special_characters(string)
        html, start, end = '', 0, len(string)
        last_spans = []
        for match in self._esc_re.finditer( string ):
            s, e = match.span()
            add = string[ start : s ]
            # log.debug(f"{add = }")
            html += add
            start = e

            reset, span = self._esc_to_span( match.group() )
            if reset:
                html = self._end_spans( hb )
            html += span

        self._reset()
        return self._end_spans( html + string[ start : end ])

    def save( self, path = '', *, overwrite = False, to_pdf = False ):
        if not ( self.saved or path ):
            raise ValueError("No file path set yet for saving!")

        if path:
            path = Path(path).absolute()
            if not path.parent.is_dir():
                raise FileNotFoundError(f"Parent folder '{path.parent}' doesn't exist!")
            path = path.parent.joinpath( f"{path.stem}.html" )

        else:
            path = self.saved

        save_path = path


        tmp = tmpfile( mode = 'w', delete = False, suffix = path.suffix )
        with self as f:
            tmp.write( f.read() )
        tmp.close()

        try:
            if to_pdf:
                toPDF( tmp.name, path, overwrite = overwrite )

            else:
                if path.exists() and path.is_dir():
                    raise NameError(f"Destination path '{path}' is a directory")
                elif path.exists() and not overwrite:
                    path = unique(path)

                with open( path, 'w' ) as dest, open( tmp.name, 'r' ) as src:
                    dest.write( src.read() )

                log.info(f"File written to '{path}'")

            log.info(f"Save operation completed")
            self.saved = save_path

        except Exception as E:
            log.error( E, f"Unable to save file '{path}'" )
            raise

        finally:
            os.remove( tmp.name )

def formatHtml( string, *, indent = 2, initial_indent = 0 ):
    if isinstance( indent, str ):
        IN = len(indent)
    else:
        IN = int(indent)

    if isinstance( initial_indent, str ):
        INIT = f"{'':{len(initial_indent)}}"
    else:
        INIT = f"{'':{int(initial_indent)}}"

    html = []
    string = string.strip()
    depth, start, end = 0, 0, len(string)
    last_element = ''
    for m in re.finditer( r'<.+?>', string ):
        grp = m.group()
        s, e = m.span()

        add = string[start:s]
        start = e

        if grp == '</pre>':
            if add:
                html[-1] += add

            html[-1] += grp

            depth -= IN
            if depth < 0:
                log.error(f"Indentation depth is less than 0 after '{grp}'")
                depth = 0
            last_element = grp
            continue

        elif re.match( r'^<pre(>| .*>)$', last_element ):
            if add:
                html[-1] += add
            html[-1] += grp
            continue

        elif add:
            if any( last_element.startswith(i) for i in inline_elements ):
                html[-1] += add
            else:
                html.append( f"{'':{depth}}{add}" )

        if any( grp.startswith(i) for i in inline_elements ):
            if html and ( not html[-1].endswith('>') or any( last_element.startswith(i) for i in inline_elements )):
                html[-1] += grp
            else:
                html.append( f"{'':{depth}}{grp}" )

        elif grp.endswith('/>') or any( grp.startswith(i) for i in void_elements ):
            html.append( f"{'':{depth}}{grp}" )

        elif grp.startswith('</'):
            depth -= IN
            if depth < 0:
                log.error(f"Indentation depth is less than 0 after '{grp}'")
                depth = 0

            if html[-1].startswith( f"<{grp[2:-1]}" ):
                html[-1] += grp
            else:
                html.append( f"{'':{depth}}{grp}" )

        else:
            html.append( f"{'':{depth}}{grp}" )
            depth += IN

        last_element = grp

    add = string[ start : end ]
    if add:
        if html and ( not html[-1].endswith('>') or any( last_element.startswith(i) for i in inline_elements )):
            html[-1] += add
        else:
            html.append( f"{'':{depth}}{add}" )

    if INIT:
        html = [ f"{INIT}{i}" for i in html ]

    return '\n'.join(html)

def ansi2html( string ):
    AH = AnsiHtml()
    return AH.parse_string( string )

__all__ = [ 'AnsiHtml',
            'HtmlTheme',
            'HtmlThemes',
            'ansi2html',
            ]
