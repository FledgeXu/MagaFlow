import os
from pathlib import Path
from typing import Generator

from .types import PathLike


def fast_scan(folder_path: PathLike) -> Generator[Path, None, None]:
    for entry in os.scandir(folder_path):
        if entry.is_file(follow_symlinks=False):
            yield Path(entry.path)
        elif entry.is_dir(follow_symlinks=False):
            yield from fast_scan(entry.path)
