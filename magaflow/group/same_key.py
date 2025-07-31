from collections import defaultdict
from typing import Dict, Iterable, List

from ..core.file_asset import FileAsset
from ..core.sample import Sample


class SameKeyGroupStrategy:
    def group(self, assets: Iterable["FileAsset"]) -> List["Sample"]:
        sample_dict: Dict[str, Dict[str, list]] = defaultdict(lambda: defaultdict(list))
        for asset in assets:
            for group_key in asset.group_keys:
                sample_dict[group_key][asset.category].append(asset)
        return [Sample(key, value) for key, value in sample_dict.items()]
