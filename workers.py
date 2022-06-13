import utilities as u
import requests
import json


def create_workers(api_key, file):

    data_tuple = u.read_file(file)
    worker_count = data_tuple[0]
    workers = data_tuple[1]

    print("Number of workers: " + str(worker_count))

    for w in workers:
        try:

            url = "https://onfleet.com/api/v2/workers"

            payload = json.dumps({'name': w['name'], 'phone': w['phone'], "teams": w['teams'], "vehicle": w[
                'vehicle'], 'capacity': w['capacity']})

            headers = {
                'Authorization': 'Basic ' + u.encode_b64(api_key),
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


def list_workers():
    url = "https://onfleet.com/api/v2/workers?filter=id"
    payload = ""
    headers = {
        'Authorization': 'Basic ' + u.encode_b64(api_key)
    }

    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

    return response


def delete_workers(api_key, workerid=None):

    if workerid:
        url = f"https://onfleet.com/api/v2/workers/{workerid}"

        payload={}
        headers = {
            'Authorization': 'Basic ' + u.encode_b64(api_key)
        }

        response = json.loads(requests.request("DELETE", url, headers=headers, data=payload).text)
        # print(response)
        print("Worker " + workerid + " deleted.")
    else:
        confirm = input("Delete all workers? y or n. ")

        if confirm == "y":
            workers = list_workers()

            for w in workers:
                workerid = w['id']

                url = f"https://onfleet.com/api/v2/workers/{workerid}"

                payload = {}
                headers = {
                    'Authorization': 'Basic ' + u.encode_b64(api_key)
                }

                response = json.loads(requests.request("DELETE", url, headers=headers, data=payload).text)
                # print(response)
                print("Worker " + w['id'] + " deleted.")


