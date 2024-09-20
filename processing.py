"""
Utils for extracting structured responses from LLM output.
"""
from typing import List
import re
import json

from utils import load_jsonl, dump_jsonl
from library import NLLemma


######## Lemma extraction

def extract_lemma_from_output(output: str):
    lemmas = output.split("\n\n")
    lemmas = [re.findall(r"<lemma>([\w\W]*)</lemma>", l) for l in lemmas]
    lemmas = [l[0] for l in lemmas if len(l) > 0]
    try:
        if len(lemmas) > 0:
            return [NLLemma(**json.loads(lemma)) for lemma in lemmas]
    except json.JSONDecodeError:
        pass
    # For some reason Qwen-2 likes this alternative format
    statements = re.findall(r"\*\*Statement\*\*:([^*]*)(\*\*)?", output)
    proofs = re.findall(r"\*\*Proof\*\*:([^*]*)(\*\*)?", output)
    descriptions = re.findall(r"\*\*Description\*\*:([^#]*)(###)?", output)
    if len(statements) != len(proofs) or len(proofs) != len(descriptions):
        return None
    return [NLLemma(statement=statement[0].strip(),
                    proof=proof[0].strip(),
                    description=description[0].strip()) for statement, proof, description in zip(statements, proofs, descriptions)]


def build_library_from_outputs(outputs_path: str) -> List[NLLemma]:
    outputs = load_jsonl(outputs_path)
    print(f"Found {len(outputs)} samples")
    lemmas = [extract_lemma_from_output(output["extracted_lemmas"]) for output in outputs]
    lemmas = [lemma for lemma in lemmas if lemma is not None]
    lemmas = [e for sl in lemmas for e in sl]
    print(f"Extracted {len(lemmas)} lemmas")
    return lemmas


def extract_relevant_lemmas_from_outputs(outputs_path: str):
    outputs = load_jsonl(outputs_path)
    print(f"Found {len(outputs)} samples")
    cnt = 0
    for sample in outputs:
        sample["extracted_lemma_requests"] = re.findall(r"\*\*Lemma Description \d:\*\*([^*]*)", sample["lemma_requests"])
        cnt += len(sample["extracted_lemma_requests"])
    print(f"Found {cnt} requests")
    return outputs


def extract_lean(text) -> List[str]:
    # first split by ```lean envs
    texts = ["```lean" + t for t in text.split("```lean")]
    codes = [re.findall(r"```lean([\w\W]*)```", text) for text in texts]
    return [e for sublist in codes for e in sublist]


if __name__ == "__main__":
    data = load_jsonl("outputs/gpt_4o_vanilla_autoformalizations_lean_4.jsonl")
    for sample in data:
        try:
            sample["lean_code"] = extract_lean(sample["response"])[0]
        except IndexError:
            print("ERROR")
            sample["lean_code"] = sample["formal_statement"]
    dump_jsonl(data, "outputs/gpt_4o_vanilla_autoformalizations_lean_4.jsonl")
