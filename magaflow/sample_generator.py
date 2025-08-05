from typing import Sequence

from .core.rule import Rule
from .core.sample import Sample
from .scanner.base_scanner import BaseScanner
from .strategy.base_strategy import BaseStrategy


def sample_generator(
    scanner: BaseScanner, strategy: BaseStrategy, rules: Sequence[Rule]
) -> Sequence[Sample]:
    return strategy.group(scanner.scan(rules))
