from taskworker import TaskWorker, TypeWorker,Status
import time


def func():
    time.sleep(2)
    return 2


def callback(arg):
    print(arg)


if __name__ == "__main__":
    taskworker = TaskWorker(TypeWorker.THREAD, "114514")
    print(taskworker.status)
    taskworker.addTask({"task": func, "args": None,
                       "kwargs": None, "callback": callback})
    print(taskworker.name)
    print(taskworker.status)
    while taskworker.status == Status.PENDING:
        print(taskworker.status)
        time.sleep(1)
    else:
        print(taskworker.status)
    taskworker.close()
    print(taskworker.status)
