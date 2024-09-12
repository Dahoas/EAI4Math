from datasets import load_dataset
import requests
from typing import List
import json


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

def test_minif2f_lean4():
    sample = dataset["test"][0]
    results = query_lean_server([sample["header"]+"\n"+sample["formal_statement"]])
    print(results)
    
test_minif2f_lean4()