import taskworker
taskWorker1 = taskworker.TaskWorker(taskworker.TypeWorker.THREAD)
taskWorker2 = taskworker.TaskWorker(taskworker.TypeWorker.PROCESS)
taskWorker1.close()
taskWorker2.close()