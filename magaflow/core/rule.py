from dataclasses import dataclass, field

from .types import Extractor, Matcher


@dataclass
class Rule:
    category: str
    matcher: Matcher
    extractor: Extractor = field(default_factory=lambda: (lambda _: []))
