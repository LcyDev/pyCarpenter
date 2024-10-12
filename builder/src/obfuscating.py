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
            if CFG.obfuscator.retry:
                warn("Failed to execute Master.py... Retrying")
                return Obfuscate()
            warn("Failed to execute Master.py...")
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

    hyper_cmd = ['py', HYPERION_PATH]
    hyper_cmd.extend([
        '--rename=False',
        '--logo=False',
        f'--auto={hyperion.flags["automatic"]}',
        f'--sr={hyperion.flags["rename-vars"]}',
        f'--sc={hyperion.flags["protect-chunks"]}',
    ])

    for folder, dest in hyperion.folders.items():
        orig = Path(folder)
        pattern = '**/*.py' if dest is True else '*.py'

        for f in orig.glob(pattern):
            if dest is True:
                f_dest = output_dir / orig.relative_to(f)
            else:
                f_dest = output_dir / dest

            if f.name == '__init__.py':
                shutil.copy2(f, f_dest); continue

            cmd = hyper_cmd + [f'--file="{f}"', f'--destiny="{f_dest}/{f.name}"']
            subprocess.run(cmd)
            print()
    Test()