from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, List

from ray import ObjectRef
from returns.result import Failure, Result, Success

from magaflow.pipeline.stage_function import StageFunction


class FlowTaskState(Enum):
    WAITING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class FlowTask:
    """It's an FSM."""

    id: int
    current_stage: int
    result: Result
    state: FlowTaskState = FlowTaskState.WAITING

    def advance_state(self, stages: List[Callable]):
        if isinstance(self.result, Failure):
            self.state = FlowTaskState.FAILED
        elif self.current_stage + 1 < len(stages):
            self.current_stage += 1
            self.state = FlowTaskState.WAITING
        else:
            self.state = FlowTaskState.COMPLETED

    def launch_current_stage(self, stages: List[StageFunction]) -> ObjectRef:
        self.state = FlowTaskState.PROCESSING
        stage_fn = stages[self.current_stage]
        assert isinstance(self.result, Success), "Cannot process a failed task"
        result = self.result.unwrap()
        if not isinstance(result, tuple):
            result = (result,)
        return stage_fn.wrapper_func.remote(*result)
