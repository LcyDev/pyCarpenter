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

def app_dir() -> Path:
    if CFG.build.use_nuitka:
        return Path().resolve()
    else:
        return Path(CFG.pyinstaller.paths["output-path"]).resolve()

def full_name():
    return f'{CFG.program["name"]}_v{CFG.program["version"]}' + '_x64' if is_x64() else ''

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