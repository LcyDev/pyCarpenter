import yaml

class BuildConfig:
    class wood:
        name: str
        version: str
        dev_build: bool
        beta_build: bool

    class build:
        x64: bool
        PreTest: bool
        AutoClean: bool
        AutoRun: bool

    class package:
        folders: list[str]
        excluded: list[str]
        included: list[str]

    class python:
        x64: str
        x86: str
        show_progress: bool

    class nuitka:
        ...

    class pyinstaller:
        cfg: dict
        paths: dict
        options: dict
        extra_data: list[str]
        extra_binary: list[str]
        import_paths: list[str]
        proyect_imports: list[str]
        hidden_imports: list[str]
        extras: list[str]

CFG = BuildConfig()

def LoadConfig():
    with open(CONFIG_PATH, 'rb') as f:
        CFG = yaml.safe_load(f.read())