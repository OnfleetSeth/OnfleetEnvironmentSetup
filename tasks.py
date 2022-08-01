import json
import requests
import datetime
import time
import concurrent.futures
from utilities import rate_limited, read_file, encode_b64


@rate_limited(5)
def create_single_task(task, api_key):
    url = "https://onfleet.com/api/v2/tasks"
    payload = json.dumps(
        task
    )
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key),
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    if response == 200:
        pass
    else:
        print(datetime.datetime.now(), response.text)


def create_single_task_async(api_key, file):
    data_tuple = read_file(file)
    tasks = data_tuple[1]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        count = 0
        futures = []
        start = datetime.datetime.now()

        for task in tasks:
            futures.append(executor.submit(create_single_task, api_key=api_key, task=task))
        for future in concurrent.futures.as_completed(futures):
            print(count, future.result())

    end = datetime.datetime.now()
    print("start: " + str(start), "end: " + str(end), "duration: " + str(end-start))


def create_tasks_batch(api_key, file, batch_size=100):
    data_tuple = read_file(file)
    task_count = data_tuple[0]
    data = data_tuple[1]
    number_of_batches = (int(task_count / batch_size) + (task_count % batch_size > 0))

    print("Batch size: " + str(batch_size))
    print("Number of batches: " + str(number_of_batches))

    batch_counter = 0
    if batch_counter < number_of_batches:
        print(datetime.datetime.now(), "Trying: Create Batch " + str(batch_counter + 1) + ".")
        start = (batch_counter * batch_size)
        end = (start + batch_size) - 1

        task_batch = []
        i = start
        while i <= end:
            try:
                task_batch.append(data[i])
            except IndexError as e:
                print(e)
                break
            i += 1

        url = "https://onfleet.com/api/v2/tasks/batch"
        payload = json.dumps({"tasks": task_batch})
        headers = {
            'Authorization': 'Basic ' + encode_b64(api_key)
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.ok:
            # print(response)
            print("Batch " + str(batch_counter+1) + " created.")
            batch_counter += 1
        elif response.status_code == 404:
            # print(response)
            time.sleep(10)
            print("Batch " + str(batch_counter + 1) + " created.")
            batch_counter += 1
        elif response.status_code == 412:
            # print(response)
            print("Waiting...")
            time.sleep(5)

    print("Task creation complete.")
    return


def list_tasks(api_key):
    tasks = []
    last_id = ()
    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }

    i = 1
    while i > 0:
        if i == 1:
            url = f"https://onfleet.com/api/v2/tasks/all?from=1455072025000"
            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
            last_id = response.get('lastId', '')
            tasks = tasks + response['tasks']
            i += 1
        elif last_id != "":
            url = f"https://onfleet.com/api/v2/tasks/all?from=1455072025000&lastId={last_id}"
            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
            last_id = response.get('lastId', '')
            tasks = tasks + response['tasks']
            i += 1
        elif last_id == "":
            i = 0
    print(len(tasks))
    return tasks


def delete_tasks(api_key, task_id=None):

    if task_id:
        url = f"https://onfleet.com/api/v2/tasks/{task_id}"
        payload = {}
        headers = {
            'Authorization': 'Basic ' + encode_b64(api_key)
        }
        requests.request("DELETE", url, headers=headers, data=payload)

        print("Task " + task_id + " deleted.")

    else:
        confirm = input("Delete all tasks? y or n. ")

        if confirm == "y":
            tasks = list_tasks(api_key)
            for t in tasks:
                try:
                    task_id = t['id']
                    url = f"https://onfleet.com/api/v2/tasks/{task_id}"
                    payload = {}
                    headers = {
                        'Authorization': 'Basic ' + encode_b64(api_key)
                    }
                    requests.request("DELETE", url, headers=headers, data=payload)

                    print("Task " + task_id + " deleted.")
                except Exception as e:
                    print(e)
                    break

        print("Task deletion complete.")

    return
