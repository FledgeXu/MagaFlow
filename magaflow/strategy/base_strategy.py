from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from ..core.file import File
from ..core.sample import Sample


class BaseStrategy(ABC):
    @abstractmethod
    def group(self, files: Iterable[File]) -> Sequence[Sample]: ...
