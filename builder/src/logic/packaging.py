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
    """Add a file or directory to a zip file."""
    if path.is_file():
        zipf.write(path, path.relative_to(path.parent))
        print(f'+ "{path}"')
        return
    base_path = path.parent if include_parent else path
    print(f'Recursing directory: "{path.name}"...')
    for p in path.rglob('*'):
        zip_dest = p.relative_to(base_path)
        if destiny:
            zip_dest = destiny / zip_dest
        zipf.write(p, zip_dest)
        print(f'+ "{p}"')
    print()

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
            if not any(fnmatch.fnmatch(p, pattern) for pattern in exclusion):
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