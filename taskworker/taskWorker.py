import multiprocessing
import threading
import queue
import typing
from . import defines


def callbackWarper(callback: typing.Callable[[typing.Any], None] | None, status: dict[str, typing.Any]):
    def func(arg: typing.Any):
        if callback is not None:
            callback(arg)
        nonlocal status
        status["status"] = defines.Status.FREE
    return func


def worker(queue):
    while True:
        tk: defines.Task | None = queue.get()
        if tk is not None:
            task = tk['task']
            args = tk['args']
            kwargs = tk['kwargs']
            callback = tk['callback']
        else:
            return
        if callback is not None:
            if (not args is None) and (not kwargs is None):
                callback(task(*args, **kwargs))
            elif args is None and (not kwargs is None):
                callback(task(**kwargs))
            elif (not args is None) and kwargs is None:
                callback(task(*args))
            else:
                callback(task())
        else:
            if (not args is None) and (not kwargs is None):
                task(*args, **kwargs)
            elif args is None and (not kwargs is None):
                task(**kwargs)
            elif (not args is None) and kwargs is None:
                task(*args)
            else:
                task()


class WorkerProcess(multiprocessing.Process):
    def __init__(self, taskQueue: multiprocessing.Queue, name: str = "TaskWorker") -> None:
        self.taskQueue = taskQueue
        super().__init__(name=name)

    def setName(self,name:str):
        self.name = name

    def run(self) -> None:
        worker(self.taskQueue)


class WorkerThread(threading.Thread):
    def __init__(self, taskQueue: queue.Queue[defines.Task | None], name: str = "TaskWorker") -> None:
        self.taskQueue = taskQueue
        super().__init__(name=name)

    def run(self) -> None:
        worker(self.taskQueue)


class TaskWorker(object):
    def __init__(self, typeWorker: defines.TypeWorker) -> None:
        self.typeWorker = typeWorker
        if typeWorker == defines.TypeWorker.THREAD:
            self.taskQueue: queue.Queue[defines.Task |
                                        None] | multiprocessing.Queue[defines.Task | None] = queue.Queue()
            self.worker: WorkerProcess | WorkerThread = WorkerThread(
                self.taskQueue)

            def setName(self: typing.Self, name: str):
                self.worker.setName(name)
            self.setName = setName
            self.__status = defines.Status.FREE
        elif typeWorker == defines.TypeWorker.PROCESS:
            self.taskQueue: queue.Queue[defines.Task |
                                        None] | multiprocessing.Queue[defines.Task | None] = multiprocessing.Queue()
            self.worker: WorkerProcess | WorkerThread = WorkerProcess(
                self.taskQueue)
            self.__status = defines.Status.UNAVAILABLE
        else:
            error = ValueError()
            error.add_note("Invalid value!")
            raise error
        self.worker.start()

    @property
    def status(self: typing.Self):
        return self.__status

    def close(self) -> None:
        if self.__status == defines.Status.CLOSED:
            raise Exception()
        else:
            self.taskQueue.put(None)
            while self.worker.is_alive():
                self.worker.join()
            if isinstance(self.worker, WorkerProcess):
                self.worker.close()
            else:
                self.__status = defines.Status.CLOSED

    def addTask(self, task: defines.Task) -> None:
        if self.typeWorker == defines.TypeWorker.THREAD:
            self.__status = defines.Status.PENDING
            task['callback'] = callbackWarper(task['callback'], self.__dict__)
        self.taskQueue.put(task)
