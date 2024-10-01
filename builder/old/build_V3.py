import os, subprocess, ctypes
from json import load as jsonload
from threading import Thread
from time import sleep
from sty import *
import pathlib, shutil

CONFIG_PATH = "./config.json"
MASTERPY_DIR = "../src/wood/Master.py"
SOUNDPACKFUNCS_DIR = "../src/wood/utils/soundpack_funcs.py"
_VARSPY_DIR = "../src/wood/game/_vars.py"

compiling = False

def TitleLoop( bits: str ):
    while compiling: # Tambien odio esto.
        Title(f"Building {bits}")
        sleep(1)
        Title(f"Building {bits}.")
        sleep(1)
        Title(f"Building {bits}..")
        sleep(1)
        Title(f"Building {bits}...")
        sleep(1)

def Title(title = "pyBuilder v3.0"):
    if os.name == 'nt':
        try:
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            k32.SetConsoleTitleW(title)
            k32.SetConsoleMode(k32.GetStdHandle(-11), 7)
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'title {title}')
        os.system('color')
    else:
        sys.stdout.write(b'\33]0;' + title + b'\a')
        sys.stdout.flush()
        os.system("")

def ChangeDevMode( state: bool, bits ):
    # Deactivate/Activate dev mode
    with open(_VARSPY_DIR, 'r') as file:
        fileContent = file.read()
        file.seek(0)

        for line in file.readlines():

            lineSplited = line.lstrip().split(" ")

            if lineSplited[0] == 'devMode':
                if "True" in lineSplited[2]: value = True
                else: value = False
                fileContent = fileContent.replace( f"    devMode = {value}\n", f"    devMode = {state}\n" ) # odio esto

            elif lineSplited[0] == '"allowDev":':
                if "True" in lineSplited[1]: value = True
                else: value = False
                fileContent = fileContent.replace( f'        "allowDev": {value},\n', f'        "allowDev": {state},\n' ) # odio esto

        file.close()

    with open(_VARSPY_DIR, 'w') as file:
        file.write(fileContent)
        file.close()

    # Change the soundpacks path.
    with open(SOUNDPACKFUNCS_DIR, 'r+') as file:
        soundpacksDir = {
            True: 'SOUNDPACKS_DIR = "../src/wood/soundpacks"\n', # Dev
            False: 'SOUNDPACKS_DIR = "./soundpacks"\n' # No-dev
        }

        fileLines = file.readlines()
        fileLines[0] = soundpacksDir[state] # First line

        file.close()

    with open(SOUNDPACKFUNCS_DIR, 'w') as file:
        file.write("".join(fileLines))

    if bits == "x86":
        if not state:
            with open(MASTERPY_DIR, 'r+') as file:
                newFile = 'import os\narchitew6432 = os.environ.get("PROCESSOR_ARCHITEW6432")\nos.environ.__delitem__("PROCESSOR_ARCHITEW6432")\nos.environ.__setitem__("PROCESSOR_ARCHITEW6432",architew6432)\n'
                fileContent = file.read()
                newFile += fileContent
                file.close()

            pathlib.Path(MASTERPY_DIR).rename(MASTERPY_DIR + "tmp")

            with open(MASTERPY_DIR, 'w') as file:
                file.write(newFile)

        if state and pathlib.Path(MASTERPY_DIR + "tmp").is_file():
            os.remove(MASTERPY_DIR)
            pathlib.Path(MASTERPY_DIR + "tmp").rename(MASTERPY_DIR)

def ChangelogGenerator( file ):
    pass

def CreateBuild( bits: str ):
    buildPath = pathlib.Path(f"{config.builder['output-dir']}/{bits}")

    libPath = pathlib.Path(f"./{buildPath}/Master.dist")
    libPath = libPath.rename(f"./{buildPath}/lib")

    includePath = pathlib.Path( config.builder["include-path"] )

    for item in includePath.iterdir():
        if item.is_dir():
            shutil.copytree(item, buildPath / item.name)
        elif item.is_file():
            shutil.copy(item, buildPath / item.name)

    finalPath = f'{config.builder["output-dir"]}/Wood_{bits} {config.wood["version"]}'
    if config.wood["dev-build"]: finalPath += " DEV BUILD"
    buildPath.rename(finalPath)

def Compile( bits: str, params: list ):
    global compiling
    print(fg.li_blue, end='')
    print("╔==============================╗")
    print("│                              │")
    print("│      Building %sBits...      │" %bits[1:]) # Eliminate the "x" from bits param
    print("│                              │")
    print("╚==============================╝\n")
    print(f"{fg.red}[NOTE]: {fg.cyan}Compiling with the params: {fg.red}<<{fg.cyan} {' '.join(params)} {fg.red}>>\n{fg.rs}")

    if not config.wood["dev-build"]: ChangeDevMode( False, bits )

    flags = 0 if config.python["show-progress"] else subprocess.CREATE_NO_WINDOW
    cmd = f'{" ".join(params)} --windows-icon-from-ico="{config.builder["icon"]}" --standalone --remove-output --follow-imports --output-filename="{config.builder["output-filename"]}" --output-dir="{config.builder["output-dir"]}/{bits}" {MASTERPY_DIR}'

    compiling = True
    Thread(target=TitleLoop, args=(bits, ), daemon=True).start()
    try: subprocess.run( f'"{config.python[bits]}" -m nuitka {cmd}', creationflags=flags )
    except:
        ChangeDevMode( True, bits )
        return
    compiling = False

    ChangeDevMode( True, bits )
    CreateBuild( bits )
    # Cls()

class Config:
    python: dict
    builder: dict
    wood: dict

    def __init__( self, data: dict ):
        self.python = data["python"]
        self.builder = data["builder"]
        self.wood = data["wood"]

params = []
if config.python["x64"]: Compile("x64", params)
if config.python["x86"]: Compile("x86", params)