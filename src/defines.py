import typing
import multiprocessing


class Task(typing.TypedDict):
    task: typing.Callable
    args: typing.Tuple | None
    kwargs: typing.Dict[str, typing.Any] | None
    callback: typing.Callable[[typing.Any], None]

ProcessTaskQueue: multiprocessing.Queue = multiprocessing.Queue()
