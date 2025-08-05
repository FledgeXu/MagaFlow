from dataclasses import dataclass
from typing import Callable, List

from magaflow.core.types import PureOrPath


@dataclass
class Rule:
    category: str
    matcher: Callable[[PureOrPath], bool]
    extractor: Callable[[PureOrPath], List[str]]
