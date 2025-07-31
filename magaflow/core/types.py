import os
from typing import TypeVar, Union

PathLike = Union[str, os.PathLike]
T = TypeVar("T")
R = TypeVar("R")


class FlowRuntimeException(Exception):
    """
    封装调度过程中发生的异常，包含原始异常、traceback 以及参数信息。

    属性：
        exc (Exception): 原始异常对象。
        trackback (str): 追踪信息（traceback 字符串）。
        args (Tuple[Any, ...]): 出错函数的输入参数。
    """

    def __init__(self, exc: Exception, trackback: str = "", args: str = ""):
        super().__init__(f"{exc} | Args: {args} | Traceback: {trackback}")
