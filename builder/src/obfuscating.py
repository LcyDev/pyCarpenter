import subprocess, shutil
from pathlib import Path

from utils import error, warn, success
from config import CFG

HYPERION_PATH = "hyperion.py"

def test_result():
    if not CFG.obfuscator.testing: return

    try:
        child = subprocess.Popen(['py', 'Master.py'], cwd="obfuscated", creationflags=subprocess.CREATE_NEW_CONSOLE)
        child.communicate()[0]
        if child.returncode == 1:
            if CFG.obfuscator.retry:
                warn("Failed to execute Master.py... Retrying")
                return obfuscate()
            warn("Failed to execute Master.py...")
        else:
            success("Test completed successfully...")
    except Exception as e:
        error(e)

def create_output_dir(output_dir):
    """Create the output directory for obfuscation."""
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

def build_hyperion_command(hyperion):
    """Build the Hyperion command with the specified flags."""
    hyper_cmd = ['py', HYPERION_PATH]
    hyper_cmd.extend([
        '--rename=False',
        '--logo=False',
        f'--auto={hyperion.flags["automatic"]}',
        f'--sr={hyperion.flags["rename-vars"]}',
        f'--sc={hyperion.flags["protect-chunks"]}',
    ])
    return hyper_cmd

def obfuscate_file(file_path, dest_path, hyper_cmd):
    """Obfuscate a single file using Hyperion."""
    cmd = hyper_cmd + [f'--file="{file_path}"', f'--destiny="{dest_path}/{file_path.name}"']
    subprocess.run(cmd)
    print()

def obfuscate_folder(folder, dest, hyperion, output_dir):
    """Obfuscate files in a folder using Hyperion."""
    orig = Path(folder)
    pattern = '**/*.py' if dest is True else '*.py'

    for f in orig.glob(pattern):
        if dest is True:
            f_dest = output_dir / orig.relative_to(f)
        else:
            f_dest = output_dir / dest

        if f.name == '__init__.py':
            shutil.copy2(f, f_dest)
            continue

        obfuscate_file(f, f_dest, build_hyperion_command(hyperion))


def obfuscate():
    """Main function to obfuscate files using Hyperion."""
    hyperion = CFG.obfuscator
    output_dir = Path(hyperion.output_dir).resolve()
    create_output_dir(output_dir)

    for folder, dest in hyperion.folders.items():
        obfuscate_folder(folder, dest, hyperion, output_dir)

    test_result()