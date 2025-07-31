import os
from pathlib import Path, PurePath
from typing import Callable, Generator, Iterable, Optional, Sequence

from ..core.file_asset import FileAsset
from ..core.rule import Rule
from ..core.types import PathLike


class LocalDirectoryScanner:
    def __init__(self, root: Path, rules: Sequence[Rule]):
        self.root = root
        self.rules = rules

    def scan(
        self, progress_callback: Optional[Callable[[PurePath], None]] = None
    ) -> Iterable[FileAsset]:
        for file_path in fast_scan(self.root):
            for rule in self.rules:
                if not rule.matcher(file_path):
                    continue

                if progress_callback:
                    progress_callback(file_path)

                yield FileAsset(
                    rule.category,
                    file_path,
                    rule.extractor(file_path),
                )


def fast_scan(folder_path: PathLike) -> Generator[Path, None, None]:
    for entry in os.scandir(folder_path):
        if entry.is_file(follow_symlinks=False):
            yield Path(entry.path)
        elif entry.is_dir(follow_symlinks=False):
            yield from fast_scan(entry.path)
