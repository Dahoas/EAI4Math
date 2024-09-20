import json
from collections import defaultdict

from datasets import load_dataset


def dump_jsonl(data, filename):
    with open(filename, "w") as f:
        for sample in data:
            json.dump(sample, f)
            f.write("\n")


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


def load_data(input_path, split):
    if ".jsonl" in input_path:
        return load_jsonl(input_path)
    else:
        return list(load_dataset(input_path)[split])
    

def find_smaller_divisor(dividend, divisor):
    while dividend % divisor != 0:
        divisor -= 1
    return divisor


######## Decorators ########

def register_decorater(dict):
    def decorator(cls):
        dict[cls.name] = cls
        return cls
    return decorator
