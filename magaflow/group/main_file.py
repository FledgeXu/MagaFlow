from pathlib import PurePath
from typing import Callable, Dict, Iterable, List, Tuple

from ..core.file_asset import FileAsset
from ..core.sample import Sample


class MainFileGroupStrategy:
    def __init__(
        self,
        main_file_category: str,
        matcher: Callable[[PurePath], List[str]],
        name_fn: Callable[[PurePath], str] = lambda p: p.stem,
    ):
        self.main_file_category = main_file_category
        self.matcher = matcher
        self.name_fn = name_fn

    def group(self, assets: Iterable["FileAsset"]) -> List["Sample"]:
        main_files = []
        other_files = []
        for asset in assets:
            if asset.category == self.main_file_category:
                main_files.append(asset)
            else:
                other_files.append(asset)

        sample_dict: Dict[Tuple[str, ...], "Sample"] = dict()
        for main in main_files:
            sample_name = self.name_fn(main.path)
            group_keys = tuple(self.matcher(main.path))  # 转换为可哈希的键
            if group_keys not in sample_dict:
                sample_dict[group_keys] = Sample(name=sample_name)
            sample_dict[group_keys].file_assets[self.main_file_category].append(main)

        for other in other_files:
            for key in other.group_keys:
                for sample_key in sample_dict:
                    if key in sample_key:
                        sample_dict[sample_key].file_assets[other.category].append(
                            other
                        )

        return list(sample_dict.values())
