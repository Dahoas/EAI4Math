from gptquery import GPT
from utils import load_jsonl

PROBLEM_KEY_NAME = "question"
SOLUTION_KEY_NAME = "answer"
OUTPUT_KEY_NAME = "extracted_lemmas"

input_path = "data/filtered_math_prm_test_2.jsonl"
data = load_jsonl(input_path)  # assumes problems is given in 'question' field

task_prompt_text = f"""\
You are a top maths student. You are shown the following question + answer pair
Problem:
{PROBLEM_KEY_NAME}
Solution:
{SOLUTION_KEY_NAME}
Using your extensive knowledge of mathematics, you must go through the solution and 
annotate sub-parts which can be extracted as tactics/lemmas of independent interest that may
be useful for solving other math questions. Enclose the statement of each lemma in the <lemma>LEMMA_STATEMENT</lemma>
tag. If a corresponding proof is available, enclose the proof subsequently in <proof>PROOF</proof>.
"""
model_name = "openai/casperhansen/llama-3-70b-instruct-awq"
max_num_tokens = 1536
logging_path = "MATH_lemma_extract.jsonl"
model = GPT(model_name=model_name,
            task_prompt_text=task_prompt_text,
            max_num_tokens=max_num_tokens,
            logging_path=logging_path,)

# query LLM
print(f"{len(data)} samples to process...")
data = model(data, output_key=OUTPUT_KEY_NAME)