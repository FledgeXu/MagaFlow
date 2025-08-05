from collections import defaultdict
from pathlib import PurePath
from typing import Dict, Iterable, Sequence

from ..core.file import File
from ..core.sample import Sample
from .base_strategy import BaseStrategy


class SameKeyStrategy(BaseStrategy):
    def group(self, files: Iterable[File]) -> Sequence[Sample]:
        sample_dict: Dict[str, Dict[str, list[PurePath]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for file in files:
            for key in file.keys:
                sample_dict[key][file.category].append(file.path)

        return [Sample(key, dict(value)) for key, value in sample_dict.items()]
