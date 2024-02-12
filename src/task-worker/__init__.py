from importlib.metadata import version

from . import cleanup as _cleanup
from .defines import MAX_WORKER, Error, Status, Task, TypeWorker
from .setting import Setting, getGlobalSetting, setGlobalSetting
from .taskWorker import TaskWorker
from .util import Table, dict2list, list2dict, list2table
from .workerPool import WorkerPoolThread

try:
    __version__ = version("TaskWorker")
except:
    __version__ = "unknown"
