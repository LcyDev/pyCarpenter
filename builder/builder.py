import os, subprocess, shutil
import yaml, pprint
import dataclasses
from sty import fg, bg

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

def CLS(new_line=True):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    if new_line:
        print()

def joinStrIf(iterable: list, body: str, string: str):
    if string: iterable.append(body%string)

def addStrIf(iterable: list, string: str, check: bool):
    if check: iterable.append(string)

def RunPyinst():
    pyinstaller = Config.pyinstaller
    PyPath = pyinstaller.paths
    flags = 0
    if Config.python["show_progress"]:
        flags |= subprocess.CREATE_NO_WINDOW
    cmd = []

    joinStrIf(cmd, "--icon %s", pyinstaller.cfg["icon"])
    joinStrIf(cmd, "--name %s", pyinstaller.cfg["app-name"])

    addStrIf(cmd, "--noconfirm", pyinstaller.options["confirm-replace"])
    addStrIf(cmd, "--clean", pyinstaller.options["clean"])
    addStrIf(cmd, "--onefile", pyinstaller.options["onefile-mode"])
    joinStrIf(cmd, "--log-level %s", pyinstaller.options["log-level"])

    joinStrIf(cmd, "--distpath %s", PyPath["output-path"])
    joinStrIf(cmd, "--workpath %s", PyPath["work-path"])
    joinStrIf(cmd, "--specpath %s", PyPath["spec-path"])
    joinStrIf(cmd, "--contents-directory %s", PyPath["contents-dir"])

    cmd.extend([f'--add-data {i}' for i in pyinstaller.extra_data if i])
    cmd.extend([f'--add-binary {i}' for i in pyinstaller.extra_binary if i])
    cmd.extend([f'--paths {i}' for i in pyinstaller.import_paths if i])
    cmd.extend([f'--hidden-import={i}' for i in pyinstaller.proyect_imports if i])
    cmd.extend([f'--hidden-import={i}' for i in pyinstaller.hidden_imports if i])
    cmd.extend([i for i in pyinstaller.extras if i])

def Compile():
    print()
    if not Config.wood["dev-build"]: ChangeDevMode(False, )

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

if __name__ == '__main__':
    LoadConfig()
    Splash()