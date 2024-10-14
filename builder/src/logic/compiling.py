from config import CFG, DEBUG, Work
from utils import CLS, addStrIf, joinIfStr, extIfStr

from logic.toggling import SetDevMode, SetIsCompiled

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

    addStrIf(cmd, "--clean", pyins.options["clean"])
    addStrIf(cmd, "--noconfirm", pyins.options["no-confirm"])
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

    if isinstance(pyins.cfg["script"], list):
        cmd.extend(pyins.cfg["script"])
    return cmd

def Compile():
    if not CFG.program.dev_build:
        SetDevMode(False)
    SetIsCompiled(True)
    print(...)
    SetIsCompiled(False)