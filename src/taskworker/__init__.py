from . import cleanup as _cleanup
from .defines import MAX_WORKER, Task, TypeWorker, Status, Error
from .setting import Setting, getGlobalSetting, setGlobalSetting
from .taskWorker import TaskWorker
from .util import Table, dict2list, list2dict, list2table
from .workerPool import WorkerPoolThread

__version__ = "0.0.1b"