from dataclasses import dataclass
from enum import Enum, auto

from returns.result import Result


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
