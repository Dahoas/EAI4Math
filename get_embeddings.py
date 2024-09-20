from openai import OpenAI
from tqdm import tqdm
import argparse

from utils import load_jsonl, dump_jsonl


def run(input_path,
        input_key,):
    client = OpenAI()
    data = load_jsonl(input_path)
    for sample in tqdm(data):
        result = client.embeddings.create(
            input=sample[input_key], model="text-embedding-3-large"
        ).data
        embeddings = [sample.embedding for sample in result]
        if isinstance(sample[input_key], list):
            sample["embeddings"] = embeddings
        else:
            sample["embedding"] = embeddings[0]
    embeddings_path = input_path.split(".jsonl")[0]
    embeddings_path = f"{embeddings_path}_embeddings.jsonl"
    dump_jsonl(data, embeddings_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default="outputs/test_extracted_lemma_descriptions.jsonl")
    parser.add_argument("--input_key", type=str, default="extracted_lemma_requests")
    
    args = parser.parse_args()
    run(**vars(args))
