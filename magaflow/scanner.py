from pathlib import PurePath
from typing import Callable, Generator, Optional, Sequence

from .core.file_asset import FileAsset
from .core.rule import Rule
from .core.types import PathLike
from .core.utils import fast_scan


def scan_local_files(
    input_dir: PathLike,
    rules: Sequence[Rule],
    process_callback: Optional[Callable[[PurePath], None]] = None,
) -> Generator[FileAsset, None, None]:
    for file_path in fast_scan(input_dir):
        matched = next((rule for rule in rules if rule.matcher(file_path)), None)
        if matched:
            if process_callback:
                process_callback(file_path)
            yield FileAsset(matched.category, file_path, matched.extractor(file_path))
