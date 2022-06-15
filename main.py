import tasks
import workers

api_key = "b4523670d4ba81be1c6a2084776093eb"

tasks_filepath = "/Users/sethlipman/Desktop/tasks.json"
workers_filepath = "/Users/sethlipman/Desktop/workers.json"

# Clear Out Environment
# None = delete all
# tasks.delete_tasks(api_key=api_key, taskid=None)
workers.delete_workers(api_key=api_key, workerid=None)

# Setup Environment
# tasks.create_tasks_batch(api_key=api_key, file=tasks_filepath, batchsize=100)
# workers.create_workers(api_key=api_key, file=workers_filepath)
