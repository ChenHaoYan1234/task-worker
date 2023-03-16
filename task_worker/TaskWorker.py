import multiprocessing
import threading
import queue
from . import defines


class WorkerProcess(multiprocessing.Process):
    def __init__(self, taskQueue: multiprocessing.Queue) -> None:
        self.taskQueue = taskQueue
        super().__init__()

    def run(self) -> None:
        while True:
            tk: defines.Task | None = self.taskQueue.get()
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


class WorkerThread(threading.Thread):
    def __init__(self, taskQueue: queue.Queue[defines.Task | None]) -> None:
        self.taskQueue = taskQueue
        super().__init__()

    def run(self) -> None:
        while True:
            tk: defines.Task | None = self.taskQueue.get()
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

class TaskWorker(object):
    def __init__(self,typeWorker:defines.TypeWorker) -> None:
        if typeWorker == defines.TypeWorker.THREAD:
            self.TaskQueue:queue.Queue[defines.Task] = queue.Queue()

def getNewWorker(typeWorker: defines.TypeWorker):
    if typeWorker == defines.TypeWorker.PROCESS:
        TaskQueueProcess: multiprocessing.Queue[defines.Task |
                                                None] = multiprocessing.Queue()
        TaskWorkerProcess = WorkerProcess(TaskQueueProcess)
        TaskWorkerProcess.name = "TaskWorker"
        TaskWorkerProcess.start()
        return TaskWorkerProcess, TaskQueueProcess
    elif typeWorker == defines.TypeWorker.THREAD:
        TaskQueueThread: queue.Queue[defines.Task |
                                     None] = queue.Queue()
        TaskWorkerThread = WorkerThread(TaskQueueThread)
        TaskWorkerThread.name = "TaskWorker"
        TaskWorkerThread.start()
        return TaskWorkerThread, TaskQueueThread
