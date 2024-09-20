import argparse
import json
import os
from typing import Optional
from time import sleep
from tqdm import tqdm

from gptquery import GPT
from gptquery.utils import chunk

from prompts import prompts
from utils import load_data


def run(task_prompt_key: str,
        input_path: str, 
        split: str,
        output_path: str,
        lower: int, 
        upper: int,
        K: int,
        output_key_name: str,
        model_name: str,
        endpoint: str,
        max_num_tokens: int,
        temperature: float,
        mb_size: int,
        **kwargs,):
    data = load_data(input_path, split)[lower:upper]  # assumes problems is given in 'question' field

    local = len(endpoint) > 0
    model_name = f"openai/{model_name}" if local else model_name
    model_endpoint = endpoint if local else None

    # must prepare prompt ahead of time
    task_prompt_text = prompts[task_prompt_key]
    model = GPT(model_name=model_name,
                model_endpoint=model_endpoint,
                task_prompt_text=task_prompt_text,
                max_num_tokens=max_num_tokens,
                temperature=temperature,
                logging_path=output_path,
                mb_size=mb_size,)
    
    # repeat samples 'K' times
    data = [[sample for _ in range(K)] for sample in data]
    data = [sample for group in data for sample in group]

    # query LLM
    print(f"{len(data)} samples to process...")
    data = model(data, output_key=output_key_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", type=str, help="Path to output file.")

    parser.add_argument("--task_prompt_key", type=str, default="lemma_extraction")
    parser.add_argument("--input_path", type=str, default="hendrycks/competition_math", help="Path to jsonl containing input data.")
    parser.add_argument("--split", type=str, default="train")
    parser.add_argument("--lower", default=0, type=int, help="Start index of samples in dataset.")
    parser.add_argument("--upper", default=1_000_000_000, type=int, help="End index of samples in dataset.")

    parser.add_argument("--output_key_name", type=str, default="response")
    parser.add_argument("--K", default=1, type=int, help="Number of samples per problem.")

    parser.add_argument("--model_name", default="Qwen/Qwen2-Math-72B-Instruct")
    parser.add_argument("--endpoint", type=str, default="http://math-ord2-0:8000/v1")
    parser.add_argument("--max_num_tokens", default=1024, type=int, help="Num output tokens.")
    parser.add_argument("--temperature", default=0.7, type=float)
    parser.add_argument("--mb_size", type=int, default=16, help="Size of mini-batch querying LLM.")

    args = parser.parse_args()
    run(**vars(args))