import typing
from multiprocessing.managers import BaseManager

from . import taskWorker, workerPool


class PoolDict(typing.TypedDict):
    name: str
    pool: workerPool.WorkerPoolThread
    workers: list[taskWorker.TaskWorker]


class Setting(object):
    def __init__(self) -> None:
        self.__manager: BaseManager | None = None
        self.__worker_table: dict[str, taskWorker.TaskWorker] = {}
        self.__pool_table: dict[str, PoolDict] = {}

    @property
    def manager(self):
        if isinstance(self.__manager, BaseManager):
            return self.__manager
        else:
            error = ValueError("Manager isn't inited!")
            raise error

    @manager.setter
    def manager(self, value: BaseManager):
        if isinstance(value, BaseManager):
            self.__manager = value
        else:
            error = TypeError("")  # !TODO Add a error message.
            raise error

    def register(self, obj: taskWorker.TaskWorker | workerPool.WorkerPoolThread, name: str):
        if isinstance(obj, taskWorker.TaskWorker):
            self.__worker_table[name] = obj
        elif isinstance(obj, workerPool.WorkerPoolThread):
            self.__pool_table[name] = {
                "name": name,
                "pool": obj,
                "workers": obj.workers
            }

    def unregister(self, obj: taskWorker.TaskWorker | workerPool.WorkerPoolThread):
        if isinstance(obj, taskWorker.TaskWorker):
            for key, value in self.__worker_table.items():
                if value == obj:
                    del self.__worker_table[key]
                    break
        elif isinstance(obj, workerPool.WorkerPoolThread):
            for key, item in self.__pool_table.items():
                if item["pool"] == obj:
                    del self.__pool_table[key]
                    break

    @property
    def worker_table(self):
        return self.__worker_table

    @property
    def pool_table(self):
        return self.__pool_table


_GLOBAL_SETTING = Setting()


def getGlobalSetting():
    return _GLOBAL_SETTING


def setGlobalSetting(setting: Setting):
    if isinstance(setting, Setting):
        global _GLOBAL_SETTING
        _GLOBAL_SETTING = setting
    else:
        error = TypeError("Unknow type!")
        raise error
