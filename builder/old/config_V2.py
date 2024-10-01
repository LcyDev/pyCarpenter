#https://github.com/adang1345/PythonWindows/blob/master/3.8.16
pyPaths = {
    "Ins32": "pyinstaller.exe",
    "Ins64": "",
    # Add to system variables or set here
    "rar": "rar",
    "7zip": "7zip",
    "hyperion": "utils/hyperion.py"
}

hyperion = {
    "doTesting": False,
    "automatic": True,
    "RenameVars": False,
    "ProtectChunks": False,
    "folders": {
        "../src/wood": "",
        "../src/wood/game": "game",
        "../src/wood/utils": "utils",
        "../src/wood/soundpacks": "soundpacks"
    }
}

# https://www.7-zip.org/download.html
# https://www.rarlab.com/download.htm
rarFiles = {
    #"7Zip": False, [UNSUPPORTED]
    "RAR": True,
    "exclude": [
        #"utils/data/certificate", Windows only
        "*\docs",
        "*\lang",
        "*.py",
        "*.pyc",
        "*.pyw",
    ],
    "include": [
        "utils/data/*",
        "../storage/docs/changelog.txt",
        "../storage/docs/!!! READ ME VERY IMPORTANT !!!.txt",
        "../src/resources",
    ],
    "empty": [
        "mods",
        "saves",
    ]
}

#https://pyinstaller.org/en/stable/usage.html#options
#https://pyinstaller.org/en/stable/usage.html#what-to-bundle-where-to-search
pyIns = {
#    "script": "./obfuscated/Master.py",
#    "imports": "./obfuscated",
#    "output": "./product",
#    "temp": "./utils/temp",
#    "icon": "../storage/icons/wood.ico",
#    "file-imports": [
#    ],
#    "hidden-imports": [
#    ],
#    "data": []
}