from typing import List
import argparse
import re
import numpy as np

from math_eval import math_check_equals
from utils import dump_jsonl, load_jsonl, register_decorater


metric_dict = dict()

class Metric:
    name: str
    def __init__(self):
        pass

    def __call__(self, trajectories: List[dict]):
        pass


def evaluate(sample: dict,
             task: str,
             output_key_name: str,
             solution_key_name: str,
             **kwargs,):
    """
    Wrapper around single-response, ground-truth evaluation of selected benchmarks.
    """
    if task == "MATH":
        return math_check_equals(sample[output_key_name], sample[solution_key_name])
    else:
        raise ValueError(f"Unknown task {task}!!!")
    
######## Other Metrics ########

@register_decorater(metric_dict)
class PassAt1(Metric):
    name = "pass@1"

    def __call__(self, dataset, **kwargs):
        scores = [evaluate(sample, **kwargs) for sample in dataset]
        pass_1 = np.mean(scores)
        print("pass@1: ", pass_1)
        return pass_1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, help="Path to jsonl containing input data.")
    parser.add_argument("--output_path", type=str, help="Path to output file.")
    parser.add_argument("--metric", type=str, choices=["pass@1"])
    parser.add_argument("--task", type=str, choices=["MATH"])

    parser.add_argument("--problem_key_name", type=str, default="question")
    parser.add_argument("--solution_key_name", type=str, default="answer")
    parser.add_argument("--output_key_name", type=str, default="model_answer")
    args = parser.parse_args()

    print(metric_dict)

    metric = metric_dict[args.metric]()
    data = load_jsonl(args.input_path)
    results = metric(data, **vars(args))
