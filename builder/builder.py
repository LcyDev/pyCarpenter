import os, sys
from sty import fg, bg

from src.config import CFG, Work, LoadConfig

BUILDER_VERSION = 4.0
CONFIG_PATH = "config.yml"
DEFAULT_CFG_PATH = "default.yml"

def Splash():
    LIGHT = fg(236,135,233) + '█'
    DARK = fg(170,58,253) + '█'
    BORDER = fg(96,58,253) + "━" * 56
    logo = (
        "  ██████╗ ██╗   ██╗██╗██╗     ██████╗ ███████╗██████╗  \n"
        "  ██╔══██╗██║   ██║██║██║     ██╔══██╗██╔════╝██╔══██╗ \n"
        "  ██████╔╝██║   ██║██║██║     ██║  ██║█████╗  ██████╔╝ \n"
        "  ██╔══██╗██║   ██║██║██║     ██║  ██║██╔══╝  ██╔══██╗ \n"
        "  ██████╔╝╚██████╔╝██║███████╗██████╔╝███████╗██║  ██║ \n"
        "  ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝ \0"
    ).replace('▌', LIGHT).replace('█', DARK)
    print(BORDER)
    print(logo)
    print(BORDER)
    print(f"{fg(255,67,124)} VERSION: {BUILDER_VERSION}")
    print()

def Title(text: str = f"pyCarpenter v{BUILDER_VERSION}"):
    if os.name == 'nt':
        import ctypes
        try:
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            k32.SetConsoleTitleW(text)
            k32.SetConsoleMode(k32.GetStdHandle(-11), 7)
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'title {text}')
        os.system('color')
    else:
        sys.stdout.write(b'\33]0;' + text + b'\a')
        sys.stdout.flush()
        os.system('')

def TitleLoop():
    import time
    dots = 0
    while Work.compiling:
        Title(f"Building {Work.bits}{'.'*dots}")
        dots = (dots + 1) % 4
        time.sleep(1)
    Title()

def Setup():
    LoadConfig()
    Title()
    Splash()

if __name__ == '__main__':
    Setup()