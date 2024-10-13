import os
from pathlib import Path

from config import CFG

def is_x64():
    if CFG.build.make_x64:
        return True

def is_onefile() -> bool:
    if CFG.build.use_nuitka:
        return ...
    else:
        return CFG.pyinstaller.options["onefile-mode"]

def get_full_name():
    name = f'{CFG.program["name"]}-{CFG.program["version"]}'
    if is_x64():
        name += '_x64'
    if CFG.program.dev_build:
        name += '-[DEV]'
    if CFG.program.beta_build:
        name += '-[BETA]'

def get_output_dir() -> Path:
    if CFG.build.use_nuitka:
        return Path().resolve()
    else:
        return Path(CFG.pyinstaller.paths["output-path"]).resolve()

def get_app_dir() -> Path:
    return get_output_dir() / get_full_name()

def CLS(new_line=True):
    if DEBUG: return
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    if new_line: print()

def addStrIf(iterable: list, string: str, check: bool):
    if check:
        iterable.append(string)

def joinIfStr(iterable: list, body: str, string: str):
    if string:
        iterable.append(body + f'"{string}"')

def extIfStr(iterable: list, string: str, other: list):
    iterable.extend([string + f'"{i}"' for i in other if i])