import json


dataset_path = "data/lean_workbook.json"
with open(dataset_path, "r") as f:
    dataset = json.load(f)
print(type(dataset))
print(len(dataset))
print(dataset[0].keys())
print(dataset[0]["proof"])
proof_problems = [sample for sample in dataset if len(sample["proof"]) > 0]
print(len(proof_problems))