from typing import Iterator, List, Sequence, Tuple

from returns.result import Result, Success

from ..core.sample import Sample
from .flow_task import FlowTask
from .stage_function import StageFunction


class FlowPipelineExecutor:
    def __init__(self, batch_size: int):
        import ray

        if not ray.is_initialized():
            ray.init()
        self.batch_size = batch_size
        self.stages: List[StageFunction] = []

    def register(self, func: StageFunction) -> "FlowPipelineExecutor":
        self.stages.append(func)
        return self

    def run(self, samples: Sequence[Sample]) -> Iterator[Tuple[Sample, Result]]:
        flow_tasks = [
            FlowTask(id=id(sample), current_stage=0, result=Success((sample,)))
            for sample in samples
        ]
        return
