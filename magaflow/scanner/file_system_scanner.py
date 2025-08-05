import os
from pathlib import Path
from typing import Iterable, Sequence

from magaflow.core.file import File

from ..core.rule import Rule
from ..core.types import PathLike
from .base_scanner import BaseScanner


def _fast_scan(folder_path: PathLike) -> Iterable[Path]:
    for entry in os.scandir(folder_path):
        if entry.is_file(follow_symlinks=False):
            yield Path(entry.path)
        elif entry.is_dir(follow_symlinks=False):
            yield from _fast_scan(entry.path)


class FileSystemScanner(BaseScanner):
    def __init__(self, folders: Iterable[PathLike]) -> None:
        super().__init__()
        self.folders = folders

    def scan(self, rules: Sequence[Rule]) -> Iterable[File]:
        return (
            File(rule.category, path, rule.extractor(path))
            for folder in self.folders
            for rule in rules
            for path in _fast_scan(folder)
            if rule.matcher(path)
        )
