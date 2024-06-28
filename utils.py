import json
from collections import defaultdict


def load_jsonl(filename):
    data = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            try:
                response = json.loads(line)
            except json.decoder.JSONDecodeError as e:
                print("Line num: ", i)
                raise(e)
            data.append(response)
    return data