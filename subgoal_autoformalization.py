from datasets import load_dataset
import requests
from typing import List
import json
from tqdm import tqdm
from prompts import prompts

from gptquery import GPT, FString

from utils import dump_jsonl, load_jsonl


def query_lean_server(lean_codes: List[str]):
    url = 'https://justinchiu--verifier-verify.modal.run/'
    headers = {'Content-Type': 'application/json'}
    data = [{"code": lean_code} for lean_code in lean_codes]
    data = json.dumps(data)
    
    response = requests.post(url, headers=headers, data=data)

    results = json.loads(response.text)
    return results

def preprocessed_query_lean_server(lean_codes: List[str]):
    def preprocess_lean_code(lean_code: str):
        return "import Mathlib\n" + lean_code
    return query_lean_server([preprocess_lean_code(lean_code) for lean_code in lean_codes])

def batched_query_lean_server(jsonl_path, key_name):
    url = 'https://justinchiu--verifier-verify.modal.run/'
    headers = {'Content-Type': 'application/json'}
    dataset = load_jsonl(jsonl_path)
    lean_codes = [sample[key_name] for sample in dataset]
    results = preprocessed_query_lean_server(lean_codes)
    for sample, result in zip(dataset, results):
        sample["lean_result"] = result
    return dataset

def print_prompt():
    dataset = load_dataset("cat-searcher/minif2f-lean4")
    sample = dataset["test"][2]
    prompt = FString(prompts["vanilla_autoformalization"]).format(**prompts)
    print(prompt.format(**sample))
    
    
def get_autoformalization():
    dataset = list(load_dataset("cat-searcher/minif2f-lean4")["validation"])
    task_prompt_text = str(FString(prompts["vanilla_autoformalization"]).format(**prompts))
    model = GPT(model_name="gpt-4o",
                task_prompt_text=task_prompt_text,
                logging_path="outputs/gpt_4o_vanilla_autoformalizations_lean_4.jsonl",
                max_num_tokens=4096,
                mb_size=1,)
    model(dataset)


if __name__ == "__main__":
    dataset = load_jsonl("outputs/gpt_4o_vanilla_autoformalizations_lean_4_results.jsonl")
    with open("logs/dump.log", "w") as f:
        f.write(json.dumps(dataset[175], indent=2))
    exit()
    pass_cnt, cmplt_cnt = 0, 0
    for i, sample in enumerate(dataset):
        if sample["lean_result"]["pass"]:
            pass_cnt += 1
            #print(sample["lean_code"])
        if sample["lean_result"]["complete"]:
            cmplt_cnt += 1
            #print(sample["lean_code"])
            print("Ind: ", i)
    print(pass_cnt, cmplt_cnt, len(dataset))
    exit()
    #get_autoformalization()
    #exit()
    #print_prompt()
    #exit()
    jsonl_path = "outputs/gpt_4o_vanilla_autoformalizations_lean_4.jsonl"
    dataset = batched_query_lean_server(jsonl_path, key_name="lean_code")
    dump_jsonl(dataset, "outputs/gpt_4o_vanilla_autoformalizations_results_lean_4.jsonl")