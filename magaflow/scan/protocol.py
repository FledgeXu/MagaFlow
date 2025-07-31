from pathlib import PurePath
from typing import Callable, Iterable, Optional

from typing_extensions import Protocol

from ..core.file_asset import FileAsset


class Scanner(Protocol):
    def scan(
        self, progress_callback: Optional[Callable[[PurePath], None]] = None
    ) -> Iterable[FileAsset]: ...
