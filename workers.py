import requests
import json
from utilities import read_file, encode_b64


def create_workers(api_key, file):
    data_tuple = read_file(file)
    worker_count = data_tuple[0]
    workers = data_tuple[1]

    print("Number of workers: " + str(worker_count))

    for w in workers:
        try:
            url = "https://onfleet.com/api/v2/workers"
            payload = json.dumps({'name': w['name'], 'phone': w['phone'], "teams": w['teams'], "vehicle": w[
                'vehicle'], 'capacity': w['capacity']})
            headers = {
                'Authorization': 'Basic ' + encode_b64(api_key),
                'Content-Type': 'application/json'
            }
            requests.request("POST", url, headers=headers, data=payload)

            # print(response.text)
            print("Worker (" + w['name'] + ") created.")

        except Exception as e:
            print(e)
            return

    print("Workers created.")
    return


def list_workers(api_key):
    url = "https://onfleet.com/api/v2/workers?filter=id"
    payload = ""
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text)
        # print(response.text)
        return response_json
    except Exception as e:
        print(e)


def delete_workers(api_key, worker_id=None):
    if worker_id:
        url = f"https://onfleet.com/api/v2/workers/{worker_id}"
        payload = {}
        headers = {
            'Authorization': 'Basic ' + encode_b64(api_key)
        }
        try:
            requests.request("DELETE", url, headers=headers, data=payload)
        except Exception as e:
            print(e)

        print("Worker " + worker_id + " deleted.")
    else:
        confirm = input("Delete all workers? y or n. ")

        if confirm == "y":
            workers = list_workers(api_key)

            for w in workers:
                worker_id = w['id']
                url = f"https://onfleet.com/api/v2/workers/{worker_id}"
                payload = {}
                headers = {
                    'Authorization': 'Basic ' + encode_b64(api_key)
                }

                try:
                    requests.request("DELETE", url, headers=headers, data=payload)
                    print("Worker " + w['id'] + " deleted.")
                except Exception as e:
                    print(e)
