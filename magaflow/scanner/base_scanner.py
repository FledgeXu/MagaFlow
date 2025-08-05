from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from ..core.file import File
from ..core.rule import Rule


class BaseScanner(ABC):
    @abstractmethod
    def scan(self, rules: Sequence[Rule]) -> Iterable[File]:
        pass
