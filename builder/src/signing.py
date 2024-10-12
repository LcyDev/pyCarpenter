import subprocess
from pathlib import Path
from sty import fg

from config import CFG
from utils import full_name, warn, success

SIGNER_PATH = 'signer'
CERT_PATH = 'woodcert_private.pfx'
PASSWD = 'wood_enable_CERTPAPU23958'

def Signer():
    if not Path(SIGNER_PATH).exists():
        print("https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/")
        print("Mount the ISO and open up the [Installers] folder and install the appropriate msi for [Windows App Certification Kit]")
        print("Example: Windows App Certification Kit x64-x86_en-us.msi, which installs the executable to C:/Program Files (x86)/Windows Kits/10/App Certification Kit/signtool.exe\n")
        return
    cmd = [SIGNER_PATH, 'sign', '/fd', 'SHA256', '/f', CERT_PATH, '/p', PASSWD]
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
    for i in files:
        file = Path(f'{CFG.pyinstaller.paths["output-path"]}/{full_name()}{i}.exe')
        if file.exists():
            child = subprocess.Popen(cmd + [file])
            child.communicate()[0]
            print()
            if child.returncode == 1:
                warn(f"Failed to sign file {file.name}.")
            else:
                success(f"Signed file {file.name} successfully.")
            print()