from typing import Iterable, List

from typing_extensions import Protocol

from ..core.file_asset import FileAsset
from ..core.sample import Sample


class BaseGroupStrategy(Protocol):
    def group(self, assets: Iterable["FileAsset"]) -> List["Sample"]: ...
