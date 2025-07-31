from dataclasses import dataclass
from pathlib import PurePath
from typing import List


@dataclass
class FileAsset:
    category: str
    path: PurePath
    group_keys: List[str]
