import typing
import multiprocessing

class Task(typing.TypedDict):
    task: typing.Callable
    args: typing.Tuple | None
    kwargs: typing.Dict[str, typing.Any] | None
    callback: typing.Callable[[typing.Any], None]

TaskQueue: multiprocessing.Queue = multiprocessing.Queue()
