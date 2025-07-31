from typing import Dict, Iterator, List, Sequence, Tuple, cast

import ray
from returns.result import Result, Success

from ..core.sample import Sample
from .flow_task import FlowTask, FlowTaskState
from .stage_function import StageFunction


class FlowPipelineExecutor:
    def __init__(self, batch_size: int):
        import ray

        if not ray.is_initialized():
            ray.init()
        self.batch_size = batch_size
        self._stages: List[StageFunction] = []

    def register(self, func: StageFunction) -> "FlowPipelineExecutor":
        self._stages.append(func)
        return self

    def run(self, samples: Sequence[Sample]) -> Iterator[Tuple[Sample, Result]]:
        id_to_sample = {id(sample): sample for sample in samples}
        all_tasks = [
            FlowTask(id=id(sample), current_stage=0, result=Success((sample,)))
            for sample in samples
        ]
        running_tasks: Dict[ray.ObjectRef, FlowTask] = dict()

        while True:
            waiting = [
                task for task in all_tasks if task.state == FlowTaskState.WAITING
            ]

            to_launches = waiting[: self.batch_size - len(running_tasks)]
            for task in to_launches:
                running_tasks[task.launch_current_stage(self._stages)] = task

            if not running_tasks and not any(
                f.state == FlowTaskState.WAITING for f in all_tasks
            ):
                break

            if not running_tasks:
                continue

            ready_refs, _ = ray.wait(list(running_tasks.keys()), num_returns=1)
            done_ref = ready_refs[0]
            task = running_tasks.pop(done_ref)
            task.result = cast(Result, ray.get(done_ref))

            task.advance_state(self._stages)

            if task.state in {FlowTaskState.COMPLETED, FlowTaskState.FAILED}:
                yield id_to_sample[task.id], task.result
