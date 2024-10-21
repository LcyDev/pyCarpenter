import re
from pathlib import Path

WOOD_ROOT = Path('wood/src/main/')

def ToggleFile(path: Path, defaults: dict, state: bool, type_hint: bool):
    if not path.exists():
        return
    hint = ': bool' * type_hint

    with open(path, 'r') as f:
        content = f.read()

    for key, value in defaults.items():
        pattern = rf'{key}{hint} = (True|False) # <>'
        if value is None:
            replacement = f'{key}{hint} = {state} # <>'
        else:
            replacement = f'{key}{hint} = {value} # <>'
        content = re.sub(pattern, replacement, content)

    with open(path, 'w') as f:
        f.write(content)

def SetIsCompiled(state: bool):
    master_defaults = {
        'IS_COMPILED': None,
    }
    MASTER_PY = WOOD_ROOT / 'Master.py'
    ToggleFile(MASTER_PY, master_defaults, state, type_hint=False)

def SetDevMode(state: bool):
    code_defaults = {
        # Secret
        'devMode': None,
        'allowDev': None,
        'allowMods': None,
        # Cheats
        'godMode': False,
        'passThrough': False,
        # Debug
        'doClear': True,
        'checkVersion': True,
        'saveCFG': True,
        'loadCFG': True,
    }
    CODE_PY = WOOD_ROOT / 'data/_code.py'
    ToggleFile(CODE_PY, code_defaults, state, type_hint=True)
