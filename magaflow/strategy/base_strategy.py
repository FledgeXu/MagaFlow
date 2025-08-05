from abc import ABC, abstractmethod
from typing import Iterable, List

from ..core.file import File
from ..core.sample import Sample


class GroupStrategy(ABC):
    @abstractmethod
    def group(self, files: Iterable[File]) -> List[Sample]: ...
