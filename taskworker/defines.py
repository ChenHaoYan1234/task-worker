import enum
import multiprocessing
import typing


class Task(typing.TypedDict):
    task: typing.Callable
    args: typing.Tuple | None
    kwargs: typing.Dict[str, typing.Any] | None
    callback: typing.Callable[[typing.Any], None] | None

MAX_WORKER = multiprocessing.cpu_count() - 1

class TypeWorker(enum.Enum):
    THREAD = 0
    PROCESS = 1

class Status(enum.Enum):
    PENDING = 0
    FREE = 1
    CLOSED = 2
    UNAVAILABLE = 3
