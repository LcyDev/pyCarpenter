import zipfile
import fnmatch
from pathlib import Path
from sty import fg

from config import CFG
from utils import full_name, app_dir

INCLUDE_DIR = Path('./include/')

def get_dist_file() -> Path:
    """Get the distribution file for the bundled app."""
    dist_file = Path(CFG.package.dist_dir).resolve() / f"{full_name()}.zip"
    dist_file.parent.mkdir(parents=True, exist_ok=True)
    if dist_file.exists():
        dist_file.unlink()
    return dist_file

def create_zip_file(source_dir: Path, output_file: Path):
    """Create a zip file from the source directory."""
    exclusion = CFG.package.excluded
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for i in CFG.package.included:
            # TODO: Include files and whole folders
            ...
        for root, _, files in INCLUDE_DIR.walk():
            for file in files:
                file_path = root / file
                if not any(fnmatch.fnmatch(file, pattern) for pattern in exclusion):
                    zipf.write(file_path, file_path.relative_to(INCLUDE_DIR))
        for root, _, files in source_dir.walk():
            for file in files:
                file_path = root / file
                if not any(fnmatch.fnmatch(file, pattern) for pattern in exclusion):
                    zipf.write(file_path, file_path.relative_to(source_dir))

def package():
    """Package the app."""
    source_dir = app_dir() / full_name()
    if not source_dir.exists(): return

    for folder in CFG.package.folders:
        empty = INCLUDE_DIR / folder
        empty.mkdir(parents=True, exist_ok=True)

    dist_file = get_dist_file()

    print(fg(166), end='')
    print("╔======================╗")
    print("│      APPackager      │")
    print("╚======================╝")
    print(fg.yellow)
    create_zip_file(source_dir, dist_file)