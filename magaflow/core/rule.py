from dataclasses import dataclass, field
from pathlib import PurePath
from typing import Callable, List


@dataclass
class Rule:
    category: str
    matcher: Callable[[PurePath], bool]
    extractor: Callable[[PurePath], List[str]] = field(
        default_factory=lambda: (lambda _: [])
    )
