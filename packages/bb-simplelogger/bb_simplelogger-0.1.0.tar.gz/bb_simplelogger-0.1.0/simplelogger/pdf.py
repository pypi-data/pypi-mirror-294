import sys, re, os, shlex, inspect
from tempfile import TemporaryDirectory as tempdir
from shutil import copy as CP, move as MV
from pathlib import Path
from subprocess import Popen, PIPE, run
import simplelogger
log = simplelogger.SimpleLogger(__name__)

class PDFError(Exception):
    def __init__( self, *args, **kwargs ):
        msg = ''
        for i in range( 1, len(args[:3]) + 1 ):
            if i == 3:
                msg += f"[Errno {args[-i]}] "
            elif i == 2:
                msg += f"{args[-i]}: "
            elif i == 1:
                msg += str(args[-i])
        self.msg = msg

    def __str__(self):
        return self.msg

def unique(path):
    _dir = path.parent
    name = path.stem
    ext = path.suffix

    n = 1
    while path.is_file():
        path = _dir.joinpath( f"{name} ({n}){ext}" )
        n += 1

    return path

def getSysPaths():
    pf = sys.platform
    if pf in ['win32', 'cygwin']:
        delim = ';'
    elif pf in ['darwin', 'linux']:
        delim = ':'
    else:
        raise OSError(f"Unsupported platform '{pf}' for this script")
        sys.exit(1)

    return os.environ['PATH'].split(delim)

def toPDF( src, dest, *, overwrite = False, margins = True, default_header_footer = False ):
    src = Path(src).absolute()
    dest = Path(dest).absolute()
    dest = dest.parent.joinpath( f"{dest.stem}.pdf" )

    if not dest.parent.is_dir():
        raise FileNotFoundError(f"Parent directory '{dest.parent}' doesn't exist!")
    elif dest.exists():
        if overwrite and not dest.is_file():
            raise NameError(f"Destination can not be overwritten", f"'{dest}' is not a file")
        elif not overwrite:
            dest = unique( dest )

    if not src.exists():
        raise FileNotFoundError(f"File '{src}' doesn't exist!")
    elif src.is_dir():
        raise NameError(f"Invalid source", f"'{src}' is a directory")

    apps = [ name for _list in [ os.listdir(i) for i in filter( lambda x: Path(x).is_dir(), getSysPaths() )] for name in _list ]
    prog = ''
    for name in [ 'chrome', 'chromium' ]:
        if name in apps:
            prog = name
            break

    if not prog:
        raise PDFError("Missing application", "Requires 'chrome' or 'chromium' to be installed and in system PATH")
    elif 'bash' not in apps:
        raise PDFError("Missing application", "Bash shell is required to run this script")

    opts = []
    if not margins:
        opts.append( '--no-margins' )

    if not default_header_footer:
        opts.append( '--no-pdf-header-footer' )

    cmd = [ prog, '--headless=new', '--disable-gpu', f"--print-to-pdf='output.pdf'", *opts, f"'{src.name}'" ]
    script_txt = "#!/usr/bin/bash\n\n" + " \\\n    ".join(cmd) + '\nexit $?\n'

    tmp = tempdir( delete = False )
    tmp_dir = Path(tmp.name)

    CP( src, tmp_dir.joinpath( src.name ))
    script = tmp_dir.joinpath( 'topdf.sh' )
    with open( script, 'w' ) as f:
        f.write( script_txt )

    cwd = os.getcwd()
    os.chdir(tmp_dir)
    proc = run([ 'bash', script.name ], capture_output = True, text = True )
    os.chdir(cwd)

    if proc.returncode > 0:
        raise PDFError("Error processing output", "\n          " + f"\n          ".join( stderr.split('\n') ))
    else:
        CP( tmp_dir.joinpath( 'output.pdf' ), dest )
        log.info(f"File saved as {dest}")

    os.chdir(cwd)
    tmp.cleanup()
    return dest
