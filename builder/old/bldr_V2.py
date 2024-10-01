import os, shutil, subprocess
from sty import *
from utils.funcs import *
import config



def setup():
    clear()
    if config.modules["32Bits"]:
        try:
            subprocess.call(config.pyPaths["Ins32"], creationflags=subprocess.CREATE_NO_WINDOW)
        except FileNotFoundError:
            warn("[WARN] Pyinstaller (x32) wasn't found:")
            config.modules["32Bits"] = False
    if config.modules["64Bits"]:
        try:
            subprocess.call(config.pyPaths["Ins64"], creationflags=subprocess.CREATE_NO_WINDOW)
        except FileNotFoundError:
            warn("[WARN] Pyinstaller (x64) wasn't found: ")
            config.modules["64Bits"] = False

def cReload():
    import importlib
    importlib.reload(config)
    main()

def main():
    setup()
    while True:
        print(f'{fg(160,85,212)}Version: {config.options["version"]}')
        print()
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPTIONS {fg.magenta}>>-----{fg.rs}")
        mPrint(f"[1].", f"{fg(93)}Obfuscate Code")
        mPrint("[2].", f"{fg(27)}EXECompiler")
        mPrint("[3].", f"{fg(11)}EXESigner")
        mPrint("[4].", f"{fg(166)}RARCompress")
        print()
        mPrint("[0].", f"{fg.li_red}[EXIT]")
        print()

def obfuscate():
    if not os.path.isfile(config.pyPaths["hyperion"]):
        warn("[WARN] Hyperion script wasn't found\n")
        return
    try:
        if os.path.isdir("obfuscated"):
            shutil.rmtree('obfuscated')
        os.mkdir("obfuscated")
    except Exception:
        pass
    for k, v in config.hyperion["folders"].items():
        scripts = [f.name for f in os.scandir(k) if f.is_file() and f.name.endswith((".py",".pyw",".pyx"))]
        for file in scripts:
            path = f"{k}/{file}"
            if file == "__init__.py":
                shutil.copy2(f"{k}/{file}", f"obfuscated/{v}")
                continue
            elif file in {"Master.py","_vars.py"}:
                with open(f"{k}/{file}", 'r') as f:
                    data = f.read()
                if file == "Master.py":
                    data.replace(' devPath()', ' #devPath()')
                    data.replace(' logger()', ' #logger()')
                else:
                    defaults = {
                        "devMode =": False,
                        "godMode =": False,
                        "passThrough =": False,
                        '"debugMode":': False,
                        '"allowDev":': False,
                        '"allowMP":': False,
                        '"saveCfg":': True,
                        '"loadCfg":': True,
                    }
                    for ks, vs in defaults.items():
                        data = data.replace(f"{ks} {not vs}", f"{ks} {vs}")
                with open(f"utils/{file}", 'w') as f:
                    f.write(data)
                path = f"utils/{file}"
            cmd = ['py', config.pyPaths["hyperion"], f'--file="{path}"', f'--destiny="obfuscated/{v}"', '--rename=False', f'-sr={not config.hyperion["RenameVars"]}', f'-sc={not config.hyperion["ProtectChunks"]}', f'-auto={config.hyperion["automatic"]}', '-logo=False']
            subprocess.run(cmd)
            print(fg.rs, end='')
    if os.path.isfile("utils/Master.py"):
        os.remove("utils/Master.py")
    if os.path.isfile("utils/_vars.py"):
        os.remove("utils/_vars.py")
    if config.hyperion["doTesting"]:
        try:
            child = subprocess.Popen(['py', 'Master.py'], cwd="obfuscated", creationflags=subprocess.CREATE_NEW_CONSOLE)
            child.communicate()[0]
            if child.returncode == 1:
                red("Failed to execute Master.py, retrying...\n")
                obfuscate()
            else:
                green("Test completed successfully...\n")
        except Exception as e:
            warn(f"{e}\n")
    title()


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

if __name__ == "__main__":
    title()
    main()