import multiprocessing
import queue
from . import defines


def worker(queue: multiprocessing.Queue | queue.Queue):
    while True:
        tk: defines.Task | None = queue.get()
        if tk is not None:
            task = tk['task']
            args = tk['args']
            kwargs = tk['kwargs']
            callback = tk['callback']
        else:
            return
        if (args is not None) and (kwargs is not None):
            callback(task(*args, **kwargs))
        elif args is not None:
            callback(task(*args))
        elif kwargs is not None:
            callback(task(**kwargs))
        else:
            callback(task())


ProcessTaskWorker = multiprocessing.Process(
    target=worker, args=(defines.ProcessTaskQueue,))