import yaml
from typing import Any

DEBUG = False

class Work:
    compiling: bool
    bits: str

    def set_x64(self, state: bool):
        self.bits = '64' if state else '32'

    def is_x64(self):
        return self.bits.endswith("64")

class BuildConfig:
    class program:
        name: str
        version: str
        dev_build: bool
        beta_build: bool

    class build:
        use_nuitka: bool
        make_x64: bool
        make_x86: bool
        test_before: bool
        auto_clean: bool
        auto_run: bool

    class package:
        dist_dir: str
        folders: list[str]
        excluded: list[str]
        included: list[dict[str, str]]

    class python:
        x64: str
        x86: str
        show_progress: bool

    class nuitka:
        cfg: dict[str, str]

    class pyinstaller:
        cfg: dict[str, str|list[str]]
        paths: dict[str, str]
        options: dict[str, str|bool]
        extra_data: list[str]
        extra_binary: list[str]
        import_paths: list[str]
        proyect_imports: list[str]
        hidden_imports: list[str]
        extras: list[str]

    class obfuscator:
        testing: bool
        output_dir: str
        retry: bool
        flags: dict[str, bool]
        folders: list[dict[str, str]]

CFG = BuildConfig()
WORK = Work()

def LoadConfig(path: str):
    global CFG
    with open(path, 'rb') as f:
        data = yaml.safe_load(f.read())
    CFG.__dict__.update(data)