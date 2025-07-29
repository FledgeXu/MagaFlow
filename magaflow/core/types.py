import os
from pathlib import PurePath
from typing import Any, Callable, List, Union

PathLike = Union[str, os.PathLike]

Matcher = Callable[[PurePath], bool]
Extractor = Callable[[PurePath], List[Any]]
