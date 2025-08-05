from dataclasses import dataclass
from typing import Sequence

from .types import PureOrPath


@dataclass
class File:
    category: str
    path: PureOrPath
    keys: Sequence[str]
