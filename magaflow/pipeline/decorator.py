from typing import Callable, Optional

import ray
from flow.pipline.stage_function import StageFunction
from flow.pipline.stage_function_config import StageFunctionConfig
from returns.result import safe


def pipeline_stage(name: Optional[str] = None, **resources):
    def decorator(fn: Callable):
        stage_name = name or fn.__name__
        config = StageFunctionConfig(name=stage_name, **resources)

        safe_fn = safe(fn)

        remote_fn = ray.remote(
            num_cpus=config.num_cpus, num_gpus=config.num_gpus, memory=config.memory
        )(safe_fn)

        return StageFunction(fn=fn, wrapper_func=remote_fn, config=config)

    return decorator
