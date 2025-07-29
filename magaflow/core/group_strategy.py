from typing import Iterable, List, Protocol

from .asset import FileAsset
from .sample import Sample


class GroupStrategy(Protocol):
    def group(self, assets: Iterable["FileAsset"]) -> List["Sample"]: ...
