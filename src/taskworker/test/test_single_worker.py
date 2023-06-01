import unittest
from sys import path
from .. import TaskWorker, TypeWorker

class TestSingleWorker(unittest.TestCase):
    def setUp(self):
        self.worker = TaskWorker(TypeWorker.PROCESS_TYPE)
        self.worker
