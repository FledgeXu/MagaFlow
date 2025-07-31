from dataclasses import dataclass
from typing import Callable

from ray.remote_function import RemoteFunction

from .stage_function_config import StageFunctionConfig


@dataclass
class StageFunction:
    fn: Callable
    wrapper_func: RemoteFunction
    config: StageFunctionConfig

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)
