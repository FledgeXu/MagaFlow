from collections import defaultdict
from typing import Dict, Iterable, List

from ..core.file_asset import FileAsset
from ..core.sample import Sample


class ParentDirectoryGroupStrategy:
    def __init__(self, parent_depth: int = 1, separator: str = "@"):
        self.parent_depth = parent_depth
        self.separator = separator

    def group(self, assets: Iterable["FileAsset"]) -> List["Sample"]:
        sample_dict: Dict[str, Dict[str, List["FileAsset"]]] = defaultdict(
            lambda: defaultdict(list)
        )

        for asset in assets:
            name_parts = asset.path.parts[
                -(self.parent_depth + 1) : -1
            ]  # 提取 parent_depth 层目录名
            sample_name = self.separator.join(name_parts)
            sample_dict[sample_name][asset.category].append(asset)

        return [
            Sample(name=sample_name, file_assets=file_assets)
            for sample_name, file_assets in sample_dict.items()
        ]
