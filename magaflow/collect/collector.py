from pathlib import Path
from typing import Callable, List, Optional, Sequence, Set, Tuple

from flow.core.rule import Rule
from flow.core.sample import Sample
from flow.core.types import PathLike
from flow.group.protocol import BaseGroupStrategy
from flow.group.same_key import SameKeyGroupStrategy
from flow.scan.local import LocalDirectoryScanner
from flow.scan.protocol import Scanner


def collector(
    scanner: Scanner,
    strategy: BaseGroupStrategy = SameKeyGroupStrategy(),
    progress_callback: Optional[Callable[[Path], None]] = None,
) -> List[Sample]:
    return strategy.group(scanner.scan(progress_callback))


def local_file_collector(
    intput: PathLike,
    rules: Sequence[Rule],
    strategy: BaseGroupStrategy = SameKeyGroupStrategy(),
    progress_callback: Optional[Callable[[Path], None]] = None,
) -> Tuple[List[Sample], List[Sample]]:
    scanner = LocalDirectoryScanner(Path(intput), rules)
    samples = collector(scanner, strategy, progress_callback)
    required_categories = {rule.category for rule in rules}
    return split_by_completeness(samples, required_categories)


## Utils
def split_by_completeness(
    samples: List["Sample"],
    required_categories: Set[str],
) -> Tuple[List["Sample"], List["Sample"]]:
    complete, incomplete = [], []
    for sample in samples:
        sample_categories = set(sample.file_assets.keys())
        if required_categories.issubset(sample_categories):
            complete.append(sample)
        else:
            incomplete.append(sample)
    return complete, incomplete
