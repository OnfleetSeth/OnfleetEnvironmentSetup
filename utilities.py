import base64
import json


def encode_b64(to_encode):
    encoded_ascii = to_encode.encode('ascii')
    base64_bytes = base64.b64encode(encoded_ascii)
    encoded_b64 = base64_bytes.decode('ascii')

    return encoded_b64


def read_file(file):

    f = open(file, 'r')
    data = json.loads(f.read())
    f.close()

    record_count = len(data)
    data_tuple = (record_count, data)

    return data_tuple
