import subprocess
import time
from pathlib import Path

from config import CFG, WORK
from logic.toggling import SetDevMode, SetIsCompiled
from sty import bg, fg
from utils import (
    addStrIf,
    extIfStr,
    get_app_dir,
    get_full_name,
    is_onefile,
    joinIfStr,
)


def GetFLAGS():
    flags = 0
    if not CFG.python["show_progress"]:
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

    joinIfStr(cmd, '--name=', get_full_name())
    joinIfStr(cmd, '--icon=', pyins.cfg["icon"])

    if isinstance(pyins.cfg["script"], list):
        cmd.extend(pyins.cfg["script"])
    return cmd

def EXERenamer(product: Path):
    if CFG.build.use_nuitka:
        ...
    else:
        exe = Path(product / get_full_name() + '.exe')
        exe.rename(product / CFG.pyinstaller.cfg["name"] + ".exe")

def DoStuff(x64: bool):
    WORK.set_x64(x64)
    print(fg.li_blue, end='')
    print("╔=============================╗")
    print("│                             │")
    print("│        Building with        │")
    print("│          %sBits...          │" %WORK.bits)
    print("╚=============================╝")
    print(fg.rs)
    start_time = time.perf_counter()
    flags = GetFLAGS()
    if CFG.build.use_nuitka:
        cmd = GetCMD_Nuitka()
    else:
        cmd = GetCMD_PyIns()
    WORK.compiling = True
    result = subprocess.run(cmd, creationflags=flags)
    product = get_app_dir()
    if not is_onefile():
        EXERenamer(product)
    WORK.compiling = False
    if result.returncode == 1:
        print('Failed to build "{product}" using params:')
        print(f"{fg.red}<< {fg.cyan}{' '.join(cmd)} {fg.red}>>")
        print(fg.rs)
        return False
    else:
        time_taken = time.perf_counter() - start_time
        print(f'Successfully Built "{product}" in {time_taken}')
        print(fg.rs)
        return True

def Compile():
    # Setup
    SetIsCompiled(True)
    SetDevMode(CFG.program.dev_build)
    # Compile
    if CFG.build.make_x64:
        DoStuff(True)
    if CFG.build.make_x86:
        DoStuff(False)
    # End
    SetIsCompiled(False)