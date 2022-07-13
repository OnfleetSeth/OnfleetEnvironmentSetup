import tasks
import workers

# Onfleet API key
API_KEY = "24bb3ed7b12129427d449c91e948a7bb"

# JSON formatted lists of entities to create
TASKS_FILEPATH = "/Users/sethlipman/Desktop/tasks.json"
WORKERS_FILEPATH = "/Users/sethlipman/Desktop/workers.json"

# Clear Out Environment
# Provide taskId or workerID to delete single task/worker, provide None to delete ALL tasks/workers
# tasks.delete_tasks(api_key=API_KEY, task_id=None)
# workers.delete_workers(api_key=API_KEY, worker_id=None)

# Setup Environment
# tasks.create_single_task_async(api_key=API_KEY, file=TASKS_FILEPATH)
# tasks.create_tasks_batch(api_key=API_KEY, file=TASKS_FILEPATH, batch_size=100)
# workers.create_workers(api_key=API_KEY, file=WORKERS_FILEPATH)

