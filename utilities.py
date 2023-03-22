import base64
import json
import time


def encode_b64(to_encode):
    encoded_ascii = to_encode.encode('ascii')
    base64_bytes = base64.b64encode(encoded_ascii)
    encoded_b64 = base64_bytes.decode('ascii')

    return encoded_b64


def read_file(file):
    f = open(file, 'r')
    data = json.loads(f.read())
    f.close()

    # Almost always helpful to know the number of tasks in the batch, so including in tuple
    record_count = len(data)
    data_tuple = (record_count, data)

    return data_tuple


def rate_limited(max_per_second):
    min_interval = 1.0 / float(max_per_second)

    def decorate(func):
        last_time_called = [0.0]

        def rate_limited_function(*args, **kwargs):
            elapsed = time.time() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_time_called[0] = time.process_time()
            return ret
        return rate_limited_function

    return decorate
