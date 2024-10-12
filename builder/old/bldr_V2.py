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