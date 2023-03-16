import multiprocessing
import threading
import queue
from . import defines


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
    def __init__(self, taskQueue: multiprocessing.Queue, name:str = "TaskWorker") -> None:
        self.taskQueue = taskQueue
        super().__init__(name=name)

    def run(self) -> None:
        worker(self.taskQueue)


class WorkerThread(threading.Thread):
    def __init__(self, taskQueue: queue.Queue[defines.Task | None], name:str = "TaskWorker") -> None:
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

        elif typeWorker == defines.TypeWorker.PROCESS:
            self.taskQueue: queue.Queue[defines.Task |
                                        None] | multiprocessing.Queue[defines.Task | None] = multiprocessing.Queue()
            self.worker: WorkerProcess | WorkerThread = WorkerProcess(
                self.taskQueue)
        else:
            error = ValueError()
            error.add_note("Invalid value!")
            raise error
        self.worker.start()

    def close(self) -> None:
        self.taskQueue.put(None)
        while self.worker.is_alive():
            self.worker.join()
        if self.typeWorker == defines.TypeWorker.PROCESS:
            self.worker.close()

    def addTask(self, task: defines.Task) -> None:
        self.taskQueue.put(task)
