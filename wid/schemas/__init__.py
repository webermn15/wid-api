import os
import json


def load_schema(filename):
    schema_path = os.path.dirname(__file__)
    path = os.path.join(schema_path, '{}.json'.format(filename))

    with open(os.path.abspath(path), 'r') as fp:
        data = fp.read()

    return json.loads(data)
