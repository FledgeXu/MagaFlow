from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from magaflow.core.types import PureOrPath


@dataclass
class Sample:
    name: str
    files: Dict[str, List[PureOrPath]] = field(default_factory=dict)

    @property
    def category(self) -> tuple[str, ...]:
        return tuple(self.files.keys())

    @property
    def paths(self) -> Iterable[PureOrPath]:
        return (path for paths in self.files.values() for path in paths)

    def add_file(self, category: str, file_path: PureOrPath):
        self.files.setdefault(category, list()).append(file_path)

    @classmethod
    def from_merged(
        cls, samples: Iterable["Sample"], name: Optional[str] = None
    ) -> "Sample":
        merged_files: Dict[str, List[PureOrPath]] = defaultdict(list)
        for sample in samples:
            for category, assets in sample.files.items():
                merged_files[category].extend(assets)

        merged_name = name or "+".join(sorted(set(s.name for s in samples)))
        return Sample(name=merged_name, files=dict(merged_files))
