from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import PurePath
from typing import Dict, List, Optional, Sequence, Set

from .asset import FileAsset


@dataclass
class Sample:
    name: str
    file_assets: Dict[str, List[FileAsset]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def __post_init__(self):
        self._files_cache = None

    @property
    def files(self) -> Dict[str, List[PurePath]]:
        if self._files_cache is None:
            result = defaultdict(list)
            for category, assets in self.file_assets.items():
                for asset in assets:
                    result[category].append(asset.path)
            self._files_cache = dict(result)
        return self._files_cache

    @property
    def categories(self) -> Set[str]:
        return set(self.file_assets.keys())

    @property
    def paths(self) -> List[PurePath]:
        return [asset.path for assets in self.file_assets.values() for asset in assets]

    @staticmethod
    def from_merged(
        samples: Sequence["Sample"], name: Optional[str] = None
    ) -> "Sample":
        merged_assets: Dict[str, List[FileAsset]] = defaultdict(list)
        for sample in samples:
            for category, assets in sample.file_assets.items():
                merged_assets[category].extend(assets)

        merged_name = name or "+".join(sorted(set(s.name for s in samples)))
        return Sample(name=merged_name, file_assets=merged_assets)
