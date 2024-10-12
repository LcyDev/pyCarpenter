import os, shutil, subprocess
from sty import *
from utils.funcs import *
import config

def build(x64=False):
    fullname = f'{config.options["name"]} v{config.options["version"]}'
    if x64:
        fullname += "_x64"
    product = f'{config.pyIns["output"]}/{fullname}'
    try:
#        if config.options["CleanRoom"]:
#            if os.path.isfile(f"{fullname}.spec"):
#                os.remove(f"{fullname}.spec")
#            if os.path.isdir(config.pyIns["temp"]):
#                shutil.rmtree(config.pyIns["temp"])
        if config.hyperion["doTesting"]:
            exe = None
            if os.path.isfile(f"{product}/{fullname}.exe"):
                exe = f"{product}/{fullname}.exe"
            elif os.path.isfile(f'{product}/{config.LIB["Launcher"]}.exe'):
                exe = f'{product}/{config.LIB["Launcher"]}.exe'
            if exe is None:
                warn("Couldn't find executable to test")
            else:
                try:
                    child = subprocess.Popen(exe, cwd=product, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    child.communicate()[0]
                    if child.returncode == 1:
                        red("Failed to execute Program, retrying...\n")
                        obfuscate()
                    else:
                        green("Test completed successfully...\n")
                except Exception as e:
                    warn(f"{e}\n")
        title()
    except Exception as e:
        warn(f"{e}\n")

def signer(x64=False):
    if not os.path.isfile(config.pyPaths["signer"]):
        print("https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/")
        print("Mount the ISO and open up the [Installers] folder and install the appropriate msi for [Windows App Certification Kit]")
        print("Example: Windows App Certification Kit x64-x86_en-us.msi, which installs the executable to C:/Program Files (x86)/Windows Kits/10/App Certification Kit/signtool.exe\n")
        return
    else:
        fullname = f'{config.options["name"]} v{config.options["version"]}'
        if x64:
            fullname += "_x64"
        cmd = [config.pyPaths["signer"], 'sign', '/fd', 'SHA256', '/f', '../storage/private/woodcert_private.pfx', '/p', 'wood_enable_CERTPAPU23958']
        dirs = [
            '.exe',
            f'/{config.options["name"]}.exe',
            f'/{config.LIB["Launcher"]}.exe',
            f'/{fullname}.exe',
            f'/{config.LIB["libDir"]}/{config.options["name"]}.exe',
        ]
    try:
        print(fg(11), end='')
        print("╔=====================╗")
        print("│      EXESigner      │")
        print("╚=====================╝")
        print(fg.yellow)
        for i in dirs:
            if os.path.isfile(f'{config.pyIns["output"]}/{fullname}{i}'):
                subprocess.run([*cmd, f'{config.pyIns["output"]}/{fullname}{i}'])
                print()
    except Exception as e:
        warn(f"{e}\n")

def rar(x64=False):
    if not os.path.isdir("dist"):
        os.mkdir("dist")
    fullname = f'{config.options["name"]} v{config.options["version"]}'
    excluded = list(f"-x{i}" for i in config.rarFiles["exclude"])
    if x64:
        fullname += "_x64"
    product = f'{config.pyIns["output"]}/{fullname}'
    #if config.rarFiles["7Zip"]:
    #    cmd = [config.pyPaths["7zip"], "a"]
    if config.rarFiles["RAR"]:
        cmd = [config.pyPaths["rar"], "a", "-ep1", "-r", *excluded]
    if os.path.isfile(f"dist/{fullname}.rar"):
        os.remove(f"dist/{fullname}.rar")
    try:
        for i in config.rarFiles["empty"]:
            os.makedirs(f"utils/data/{i}", exist_ok=True)
        print(fg(166), end='')
        print("╔=======================╗")
        print("│      RARCompress      │")
        print("╚=======================╝", fg.yellow)
        if os.path.isfile(f'{product}.exe'):
            subprocess.run([*cmd, f"dist/{fullname}.rar", f'{product}.exe', *config.rarFiles["include"]])
        elif os.path.isfile(f'{product}/{config.LIB["Launcher"]}.exe') and os.path.isdir(f'{product}/{config.LIB["libDir"]}'):
            subprocess.run([*cmd, f"dist/{fullname}.rar", f'{product}/{config.LIB["Launcher"]}.exe', *config.rarFiles["include"], f'{product}/{config.LIB["libDir"]}'])
        print(fg.rs)
    except Exception as e:
        warn(f"{e}\n")