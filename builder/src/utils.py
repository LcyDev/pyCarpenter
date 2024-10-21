import os
from pathlib import Path

from config import CFG, DEBUG, Work


def success(msg: str):
    ...

def warn(msg: str):
    ...

def error(e: Exception):
    ...

def Set64Bits(state: bool):
    Work.bits = '64' if state else '32'

def is_onefile() -> bool:
    if CFG.build.use_nuitka:
        return ...
    else:
        return CFG.pyinstaller.options["onefile-mode"]

def get_full_name():
    name = f'{CFG.program["name"]}-{CFG.program["version"]}'
    if CFG.program.dev_build:
        name += '-[DEV]'
    if CFG.program.beta_build:
        name += '-[BETA]'
    if Work.is_x64():
        name += '_x64'
    else:
        name += '_x86'

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

def addStrIf(target: list, item: str, condition: bool):
    """Append an item to the list if the condition is True."""
    if condition:
        target.append(item)

def joinIfStr(target: list, prefix: str, item: str):
    """Join a prefix with the item and append to the list if the item is not empty."""
    if item:
        target.append(prefix + f'"{item}"')

def extIfStr(target: list, prefix: str, items: list):
    """Extend the list with prefixed items from another list if they are not empty."""
    target.extend([prefix + f'"{i}"' for i in items if i])