import tasks
import workers

# Onfleet API key
API_KEY = "99676b6006c82a4ec9f6a5f6880b2a0f"

# JSON formatted lists of entities to create
TASKS_FILEPATH = "/Users/sethlipman/Desktop/tasks.json"
WORKERS_FILEPATH = "/Users/sethlipman/Desktop/workers.json"


def main():
    # Clear Out Environment
    # Provide taskId or workerID to delete single task/worker, provide None to delete ALL tasks/workers
    # tasks.delete_tasks(api_key=API_KEY, task_id=None)
    # workers.delete_workers(api_key=API_KEY, worker_id=None)

    # Setup Environment
    # tasks.create_single_task_async(api_key=API_KEY, file=TASKS_FILEPATH)
    tasks.create_tasks_batch(api_key=API_KEY, file=TASKS_FILEPATH, batch_size=100)
    # workers.create_workers(api_key=API_KEY, file=WORKERS_FILEPATH)


if __name__ == "__main__":
    main()
