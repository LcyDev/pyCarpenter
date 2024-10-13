import subprocess
from pathlib import Path
from sty import fg

from config import CFG
from utils import get_full_name, get_output_dir, warn, success

SIGNER_PATH = 'signer'
CERT_PATH = 'woodcert_private.pfx'
PASSWD = 'wood_enable_CERTPAPU23958'

def display_sdk_info():
    """Display information about the Windows SDK installation."""
    print("https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/")
    print("Mount the ISO and open up the [Installers] folder and install the appropriate msi for [Windows App Certification Kit]")
    print("Example: Windows App Certification Kit x64-x86_en-us.msi, which installs the executable to C:/Program Files (x86)/Windows Kits/10/App Certification Kit/signtool.exe\n")

def sign_file(file_path):
    """Sign a given file using the signing command."""
    cmd = [SIGNER_PATH, 'sign', '/fd', 'SHA256', '/f', CERT_PATH, '/p', PASSWD, file_path]
    child = subprocess.Popen(cmd)
    child.communicate()[0]
    return child.returncode

def signer():
    """Main function to sign executable files."""
    if not Path(SIGNER_PATH).exists():
        display_sdk_info()
        return

    files = [
        '',
        f'/{CFG.program["name"]}',
        f'/{CFG.pyinstaller["cfg"]["app-name"]}',
    ]

    print(fg(11), end='')
    print("╔=====================╗")
    print("│      EXESigner      │")
    print("╚=====================╝")
    print(fg.yellow)

    found = False
    output_dir = get_output_dir()
    for suffix in files:
        file_path = output_dir / f"{get_full_name()}{suffix}.exe"
        if not file_path.exists():
            continue

        found = True
        return_code = sign_file(file_path)

        if return_code == 1:
            warn(f"Failed to sign file {file_path.name}.")
        else:
            success(f"Signed file {file_path.name} successfully.")
        print()

    if not found:
        warn("No executable files found to sign.")