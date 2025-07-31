from dataclasses import dataclass
from typing import Any, Optional, Union

from flow.core.types import PathLike

Undefined: Any = object()


@dataclass
class StageFunctionConfig:
    name: str
    # Ray config
    num_cpus: Optional[Union[int, float]] = None
    num_gpus: Optional[Union[int, float]] = None
    memory: Optional[Union[int, float]] = None
    # System resource config
    cpu_load: float = float("inf")
    memory_load: float = float("inf")
    reserved_disk: float = -1
    disk_check_path: PathLike = "/"
    resource_timeout: float = float("inf")
