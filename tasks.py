import json
import requests
import datetime
import time
import pprint as p
import utilities as u


def create_tasks_batch(api_key, file, batchsize=100):

    data_tuple = u.read_file(file)
    task_count = data_tuple[0]
    data = data_tuple[1]

    number_of_batches = (int(task_count / batchsize) + (task_count % batchsize > 0))

    print("Batch size: " + str(batchsize))
    print("Number of batches: " + str(number_of_batches))

    x = 0
    while x < number_of_batches:
        print(datetime.datetime.now(), "Trying: Create Batch " + str(x + 1) + ".")
        start = (x * batchsize)
        end = (start + batchsize) - 1

        task_batch = []

        i = start
        while i <= end:
            try:
                task_batch.append(data[i])
            except IndexError:
                break

            i += 1

        url = "https://onfleet.com/api/v2/tasks/batch"

        payload = json.dumps({"tasks": task_batch})

        headers = {
            'Authorization': 'Basic ' + u.encode_b64(api_key)
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.ok:
            # print(response)
            print("Batch " + str(x+1) + " created.")
            x += 1
        elif response.status_code == 404:
            # print(response)
            time.sleep(10)
            print("Batch " + str(x + 1) + " created.")
            x += 1
        elif response.status_code == 412:
            # print(response)
            print("Waiting...")
            time.sleep(5)

    print("Task creation complete.")
    return


def list_tasks(api_key):
    tasks = []
    lastid = ()

    payload = {}
    headers = {
        'Authorization': 'Basic ' + u.encode_b64(api_key)
    }

    i = 1
    while i > 0:
        if i == 1:
            url = f"https://onfleet.com/api/v2/tasks/all?from=1455072025000"

            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

            lastid = response.get('lastId', '')

            tasks = tasks + response['tasks']

            i += 1

        elif lastid != "":

            url = f"https://onfleet.com/api/v2/tasks/all?from=1455072025000&lastId={lastid}"
            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

            lastid = response.get('lastId', '')

            tasks = tasks + response['tasks']

            i += 1
        elif lastid == "":
            i = 0

    # p.pprint(tasks)
    return tasks


def delete_tasks(api_key, taskid=None):

    if taskid:
        url = f"https://onfleet.com/api/v2/tasks/{taskid}"

        payload = {}
        headers = {
            'Authorization': 'Basic ' + u.encode_b64(api_key)
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print("Task " + taskid + " deleted.")

    else:
        confirm = input("Delete all tasks? y or n. ")

        if confirm == "y":
            tasks = list_tasks(api_key)

            for t in tasks:
                try:
                    taskid = t['id']

                    url = f"https://onfleet.com/api/v2/tasks/{taskid}"

                    payload = {}
                    headers = {
                        'Authorization': 'Basic ' + u.encode_b64(api_key)
                    }

                    requests.request("DELETE", url, headers=headers, data=payload)

                    print("Task " + taskid + " deleted.")

                except Exception as e:
                    print(e)
                    break

        print("Task deletion complete.")

    return

