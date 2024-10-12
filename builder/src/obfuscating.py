import subprocess, shutil
from pathlib import Path

from utils import error, warn, success
from config import CFG

HYPERION_PATH = "hyperion.py"

def Test():
    if not CFG.obfuscator.testing: return

    try:
        child = subprocess.Popen(['py', 'Master.py'], cwd="obfuscated", creationflags=subprocess.CREATE_NEW_CONSOLE)
        child.communicate()[0]
        if child.returncode == 1:
            warn("Failed to execute Master.py... Retry?")
            if CFG.obfuscator.retry:
                Obfuscate()
        else:
            success("Test completed successfully...")
    except Exception as e:
        error(e)

def Obfuscate():
    hyperion = CFG.obfuscator

    output_dir = Path(hyperion.output_dir).resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = ['py', HYPERION_PATH]
    cmd.append('--rename=False')
    cmd.append('--logo=False')
    cmd.append(f'--auto={hyperion.flags["automatic"]}')
    cmd.append(f'--sr={hyperion.flags["rename-vars"]}')
    cmd.append(f'--sc={hyperion.flags["protect-chunks"]}')

    for k, v in hyperion.folders.items():
        orig = Path(k)

        if isinstance(v, str):
            pattern = '*.py'
        else:
            pattern = '**/*.py'

        for f in orig.glob(pattern):
            if isinstance(v, str):
                dest = output_dir / v
            else:
                dest = output_dir / f.parent.name
            if f.name == '__init__.py':
                shutil.copy2(f, dest); continue
            x = [f'--file="{f}"', f'--destiny="{dest}/{f.name}"']
            subprocess.run(cmd + x)
            print()
    Test()