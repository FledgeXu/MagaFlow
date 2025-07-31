from typing import Callable, Optional

import ray
from returns.result import safe

from .stage_function import StageFunction
from .stage_function_config import StageFunctionConfig


def pipeline_stage(
    name: Optional[str] = None, **resources
) -> Callable[[Callable], StageFunction]:
    def decorator(fn: Callable) -> StageFunction:
        stage_name = name or fn.__name__
        config = StageFunctionConfig(name=stage_name, **resources)

        safe_fn = safe(fn)

        remote_fn = ray.remote(
            num_cpus=config.num_cpus, num_gpus=config.num_gpus, memory=config.memory
        )(safe_fn)

        return StageFunction(fn=fn, wrapper_func=remote_fn, config=config)

    return decorator
