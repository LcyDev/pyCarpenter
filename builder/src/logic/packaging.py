import zipfile
import fnmatch
from pathlib import Path
from sty import fg

from config import CFG
from utils import full_name, app_dir

INCLUDE_DIR = Path('./include/')

def get_dist_file() -> Path:
    """Get the distribution file for the bundled app."""
    dist_dir = Path(CFG.package.dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)

    dist_file = dist_dir / f"{full_name()}.zip"
    if dist_file.exists():
        dist_file.unlink()
    return dist_file

def zip_file(zipf: zipfile.ZipFile, file_path: Path, destiny: str = None):
    """Add a file to a zip file."""
    zip_dest = file_path.relative_to(file_path.parent)
    if destiny:
        zip_dest = destiny / zip_dest
    zipf.write(file_path, zip_dest)
    print(f'+ "{file_path}"')

def zip_dir(zipf: zipfile.ZipFile, dir_path: Path, include_parent: bool = True, destiny: str = None):
    """Add a directory to a zip file."""
    base_path = dir_path.parent if include_parent else dir_path
    print(f'Recursing directory: "{dir_path.name}"...')
    for path in dir_path.rglob('*'):
        zip_dest = path.relative_to(base_path)
        if destiny:
            zip_dest = destiny / zip_dest
        zipf.write(path, zip_dest)
        print(f'+ "{path}"')
    print()

def add_to_zip(zipf: zipfile.ZipFile, path: Path, include_parent: bool = True, destiny: str = None):
    if not path.exists():
        return
    elif path.is_file():
        zip_dir(zipf, path, destiny)
    elif path.is_dir():
        zip_dir(zipf, path, include_parent, destiny)

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
        for p in source_dir.rglob('*'):
            # Fixes: Exclude files & dirs.
            match = p.as_posix() + '/' if p.is_dir() else p
            if not any(fnmatch.fnmatch(match, pattern) for pattern in exclusion):
                zipf.write(p, p.relative_to(source_dir))

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