import typing
import multiprocessing
import enum

class Task(typing.TypedDict):
    task: typing.Callable
    args: typing.Tuple | None
    kwargs: typing.Dict[str, typing.Any] | None
    callback: typing.Callable[[typing.Any], None]

MAX_PROCESS = multiprocessing.cpu_count() - 1

class TypeWorker(enum.Enum):
    THREAD = 0
    PROCESS = 1
