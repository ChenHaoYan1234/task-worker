import hashlib
import multiprocessing
import queue
import random
import threading
import typing

from . import defines, setting


def hash_random() -> str:
    return hashlib.md5(str(random.random()).encode()).hexdigest()


def callbackWarper(callback: typing.Callable[[typing.Any], None] | None, status: dict[str, typing.Any]):
    def func(arg: typing.Any):
        if callback is not None:
            callback(arg)
        nonlocal status
        status["status"] = defines.Status.FREE
    return func


class WorkerProcess(multiprocessing.Process):
    def __init__(self, name: str = "TaskWorker") -> None:
        self.taskQueue: multiprocessing.Queue = multiprocessing.Queue()
        self.__status = defines.Status.FREE
        super().__init__(name=name, daemon=True)

    def put(self, task: defines.Task | None):
        self.taskQueue.put(task)

    @property
    def status(self):
        return self.__status

    def run(self) -> None:
        while True:
            tk: defines.Task | None = self.taskQueue.get()
            self.__status = defines.Status.PENDING
            if tk is not None:
                task = tk['task']
                args = tk['args']
                kwargs = tk['kwargs']
                callback = tk['callback']
            else:
                self.__status = defines.Status.CLOSED
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
            self.__status = defines.Status.FREE


class WorkerThread(threading.Thread):
    def __init__(self, name: str = "TaskWorker") -> None:
        self.taskQueue: queue.Queue[defines.Task | None] = queue.Queue()
        self.__status = defines.Status.FREE
        super().__init__(name=name, daemon=True)

    def put(self, task: defines.Task | None):
        self.taskQueue.put(task)

    @property
    def status(self):
        return self.__status

    def run(self) -> None:
        while True:
            tk: defines.Task | None = self.taskQueue.get()
            self.__status = defines.Status.PENDING
            if tk is not None:
                task = tk['task']
                args = tk['args']
                kwargs = tk['kwargs']
                callback = tk['callback']
            else:
                self.__status = defines.Status.CLOSED
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
            self.__status = defines.Status.FREE


class TaskWorker(object):
    def __init__(self, typeWorker: defines.TypeWorker, prefix: str = "TaskWorker") -> None:
        self.__name = f"{prefix}.{hash_random()}"
        self.typeWorker = typeWorker
        if typeWorker == defines.TypeWorker.THREAD:
            self.__worker: WorkerProcess | WorkerThread = WorkerThread(
                self.__name)
        elif typeWorker == defines.TypeWorker.PROCESS:
            self.__worker = WorkerProcess(self.__name)
        else:
            error = ValueError("Invalid value!")
            raise error
        self.__worker.start()
        setting.getGlobalSetting().register(self, self.__name)

    @property
    def status(self):
        return self.__worker.status
    
    @property
    def name(self):
        return self.__name

    @property
    def worker(self):
        return self.__worker

    def close(self) -> None:
        if self.__worker.status == defines.Status.CLOSED:
            raise Exception()
        else:
            self.__worker.put(None)
            while self.__worker.is_alive():
                self.__worker.join()
            if isinstance(self.__worker, WorkerProcess):
                self.__worker.close()

    def addTask(self, task: defines.Task) -> None:
        self.__worker.put(task)
