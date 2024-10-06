import os, subprocess, shutil
import yaml, pprint
import dataclasses
from sty import fg, bg

from src.utils import CLS, addStrIf, joinIfStr, extIfStr, join

DEBUG = False
BUILDER_VERSION = 4.0
CONFIG_PATH = "default.yml"

class BuildConfig:
    wood: dict
    build: dict
    python: dict
    nuitka: dict
    class pyinstaller:
        cfg: dict
        paths: dict
        options: dict
        extra_data: list[str]
        extra_binary: list[str]
        import_paths: list[str]
        proyect_imports: list[str]
        hidden_imports: list[str]
        extras: list[str]

Config = BuildConfig()

def LoadConfig():
    with open(CONFIG_PATH, 'rb') as f:
        config = yaml.safe_load(f.read())

def GetCMD_FLAGS():
    flags = 0
    if Config.python["show_progress"]:
        flags |= subprocess.CREATE_NO_WINDOW

def GetCMD_Nuitka():
    nuitka = Config.nuitka
    cmd = []
    return cmd

def GetCMD_PyIns():
    pyins = Config.pyinstaller
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
    print()
    if not Config.wood["dev-build"]: ChangeDevMode(False)

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

def set_title(text: str = ""):
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

def Setup():
    LoadConfig()
    set_title(f"pyCarpenter v{BUILDER_VERSION}")
    Splash()

if __name__ == '__main__':
    Setup()