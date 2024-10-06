import os, subprocess, shutil
from sty import fg, bg

from src.config import CFG, LoadConfig
from src.utils import CLS, addStrIf, joinIfStr, extIfStr, join


DEBUG = False
BUILDER_VERSION = 4.0

CONFIG_PATH = "config.yml"
DEFAULT_CFG_PATH = "default.yml"

class Work:
    compiling: bool
    bits: str

def GetCMD_FLAGS():
    flags = 0
    if CFG.python["show_progress"]:
        flags |= subprocess.CREATE_NO_WINDOW

def GetCMD_Nuitka():
    nuitka = CFG.nuitka
    cmd = []
    return cmd

def GetCMD_PyIns():
    pyins = CFG.pyinstaller
    if not pyins.cfg["command"]: return

    cmd = []
    cmd.append(pyins.cfg["command"])

    addStrIf(cmd, "--noconfirm", pyins.options["confirm-replace"])
    addStrIf(cmd, "--clean", pyins.options["clean"])
    addStrIf(cmd, "--onefile", pyins.options["onefile-mode"])
    joinIfStr(cmd, "--log-level=", pyins.options["log-level"])

    joinIfStr(cmd, '--distpath=', pyins.paths["output-path"])
    joinIfStr(cmd, '--workpath=', pyins.paths["work-path"])
    joinIfStr(cmd, '--specpath=', pyins.paths["spec-path"])
    joinIfStr(cmd, '--contents-directory=', pyins.paths["contents-dir"])

    extIfStr(cmd, '--add-data=', pyins.extra_data)
    extIfStr(cmd, '--add-binary=', pyins.extra_binary)
    extIfStr(cmd, '--paths=', pyins.import_paths)
    extIfStr(cmd, '--hidden-import=', pyins.proyect_imports)
    extIfStr(cmd, '--hidden-import=', pyins.hidden_imports)
    cmd.extend([i for i in pyins.extras if i])

    joinIfStr(cmd, '--name=', pyins.cfg["app-name"])
    joinIfStr(cmd, '--icon=', pyins.cfg["icon"])

    cmd.append(pyins.cfg["script"])
    return cmd

def Compile():
    if not CFG.wood["dev-build"]:
        ChangeDevMode(False)
    print()
    

def Splash():
    LIGHT = fg(236,135,233) + '█'
    DARK = fg(170,58,253) + '█'
    BORDER = fg(96,58,253) + "━" * 56
    logo = (
        "  ██████╗ ██╗   ██╗██╗██╗     ██████╗ ███████╗██████╗  \n"
        "  ██╔══██╗██║   ██║██║██║     ██╔══██╗██╔════╝██╔══██╗ \n"
        "  ██████╔╝██║   ██║██║██║     ██║  ██║█████╗  ██████╔╝ \n"
        "  ██╔══██╗██║   ██║██║██║     ██║  ██║██╔══╝  ██╔══██╗ \n"
        "  ██████╔╝╚██████╔╝██║███████╗██████╔╝███████╗██║  ██║ \n"
        "  ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝ \0"
    ).replace('▌', LIGHT).replace('█', DARK)
    print(BORDER)
    print(logo)
    print(BORDER)
    print(f"{fg(255,67,124)} VERSION: {BUILDER_VERSION}")
    print()

def Title(text: str = f"pyCarpenter v{BUILDER_VERSION}"):
    if os.name == 'nt':
        import ctypes
        try:
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            k32.SetConsoleTitleW(text)
            k32.SetConsoleMode(k32.GetStdHandle(-11), 7)
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'title {text}')
        os.system('color')
    else:
        sys.stdout.write(b'\33]0;' + text + b'\a')
        sys.stdout.flush()
        os.system('')

def TitleLoop():
    import time
    dots = 0
    while Work.compiling:
        Title(f"Building {Work.bits}{'.'*dots}")
        dots = (dots + 1) % 4
        time.sleep(1)
    Title()

def Setup():
    LoadConfig()
    Title()
    Splash()

if __name__ == '__main__':
    Setup()