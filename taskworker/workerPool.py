import typing

from . import defines, taskWorker


class WorkerPoolThread(object):
    def __init__(self, workerCount: int = defines.MAX_WORKER, prefix: str = "worker") -> None:
        self._prefix = prefix
        if workerCount > defines.MAX_WORKER:
            raise ValueError()
        self.workerType = defines.TypeWorker.THREAD
        self.workerCount = workerCount
        workers: list[taskWorker.TaskWorker] = []
        for i in range(workerCount):
            workers.append(taskWorker.TaskWorker(defines.TypeWorker.THREAD,f"{prefix}{i}"))
        self.workers = workers
        self.__closed = False

    def __getattribute__(self, __name: str) -> typing.Any:
        try:
            int(__name[len(self._prefix):])
        except:
            return object.__getattribute__(self, __name)
        else:
            if self._prefix in __name:
                id = int(__name[len(self._prefix):])
                return self.workers[id]

    def addTask(self, task: defines.Task):
        for worker in self.workers:
            if worker.status == defines.Status.FREE:
                worker.addTask(task)
                break

    @property
    def closed(self):
        return self.__closed

    def close(self):
        if self.__closed == False:
            for worker in self.workers:
                worker.close()
            self.__closed = True
        else:
            raise Exception()
