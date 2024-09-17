from datasets import load_dataset
import requests
from typing import List
import json
from tqdm import tqdm

from utils import dump_jsonl, load_jsonl


def query_lean_server(lean_codes: List[str]):
    url = 'https://justinchiu--verifier-verify.modal.run/'
    headers = {'Content-Type': 'application/json'}
    data = [{"code": lean_code} for lean_code in lean_codes]
    data = json.dumps(data)
    
    response = requests.post(url, headers=headers, data=data)

    results = json.loads(response.text)
    return results

def test_lean_server():
    lean_codes = ["import Mathlib"]
    results = query_lean_server(lean_codes)
    print(results)

#test_lean_server()

dataset = load_dataset("cat-searcher/minif2f-lean4")
print(dataset["test"][2])

def test_minif2f_lean4():
    sample = dataset["test"][2]
    results = query_lean_server(["import Mathlib\n"+sample["formal_statement"]])
    print(results)
    
#test_minif2f_lean4()

'''runs = []
for sample in tqdm(list(dataset["test"])):
    results = query_lean_server(["import Mathlib\n"+sample["formal_statement"]])
    sample["lean_results"] = results
    runs.append(sample)
    
dump_jsonl(runs, "minif2f_test_lean_results.jsonl")
    '''
    
runs = load_jsonl("minif2f_test_lean_results.jsonl")
cnt = 0
for run in runs:
    print(run)
    if run["lean_results"][0]["pass"]:
        cnt += 1
print(len(runs))
print(cnt)