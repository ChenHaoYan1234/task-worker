import taskworker
import multiprocessing
import time


def task1(arg):
    time.sleep(arg)
    def func(a): return a**2
    return func(arg)


def task2(arg):
    time.sleep(arg)
    return arg


def task3(arg):
    time.sleep(arg)
    return arg


def callback(arg):
    print(arg)


taskDict1: taskworker.Task = {
    "task": task1, "args": (1,), "kwargs": None, "callback": callback
}

taskDict2: taskworker.Task = {
    "task": task2, "args": (5,), "kwargs": None, "callback": callback
}

taskDict3: taskworker.Task = {
    "task": task3, "args": (10,), "kwargs": None, "callback": callback
}

if __name__ == "__main__":
    multiprocessing.freeze_support()
    pool = taskworker.WorkerPoolThread()
    pool.addTask(taskDict1)
    pool.addTask(taskDict2)
    pool.addTask(taskDict3)
    pool.close()
