import os, subprocess, ctypes
from json import load as jsonload
from threading import Thread
from time import sleep
from sty import *
import pathlib, shutil

MASTERPY_DIR = "../src/wood/Master.py"

compiling = False

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
    try:
        subprocess.run( f'"{config.python[bits]}" -m nuitka {cmd}', creationflags=flags )
    except Exception:
        return
    compiling = False

    CreateBuild( bits )
    # Cls()