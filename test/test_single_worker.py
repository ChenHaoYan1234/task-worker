import unittest
import typing
from .. import TaskWorker, TypeWorker, Task, Status


def callback(value: dict):
    def _(arg: typing.Any):
        nonlocal value
        value["value"] = arg
    return _


class TestSingleWorker(unittest.TestCase):
    def setUp(self):
        self.worker = TaskWorker(TypeWorker.PROCESS_TYPE)
        self.value = 0

    def testLambda(self):
        task: Task = {
            "task": lambda: 0,
            "args": None,
            "kwargs": None,
            "callback": callback(self.__dict__)
        }
        self.worker.addTask(task)
        while not self.worker.status == Status.FREE:
            pass
        else:
            self.assertEqual(self.value, 0)
    
