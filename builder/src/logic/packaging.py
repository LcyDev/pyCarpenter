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

def add_to_zip(zipf: zipfile.ZipFile, path: Path, include_parent: bool = True, destiny: str = None):
    if path.is_file():
        zipf.write(path, path.relative_to(path.parent))
        return
    relative = path.parent if include_parent else path
    for root, _, files in path.walk():
        for f in files:
            file_path = root / f
            if destiny:
                zipf.write(file_path, destiny / file_path.relative_to(relative))
            else:
                zipf.write(file_path, file_path.relative_to(relative))

def create_zip_file(source_dir: Path, output_file: Path):
    """Create a zip file from the source directory."""
    exclusion = CFG.package.excluded
    inclusion = CFG.package.included
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for orig, dest in inclusion.items():
            wild = orig.endswith('*')
            path = Path(orig[:-1] if wild else orig)
            destiny = dest if isinstance(dest, str) else None
            add_to_zip(zipf, path, include_parent=not wild, destiny=destiny)
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