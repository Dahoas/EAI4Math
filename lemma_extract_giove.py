import argparse
import transformers
import torch

from utils import load_jsonl

# Keys in the MATH dataset
PROBLEM_KEY_NAME = "question"
SOLUTION_KEY_NAME = "answer"


def main():
    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"  # https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct

    parser = argparse.ArgumentParser('Extract lemmas from examples in the MATH dataset.')
    parser.add_argument('-e', '--extract', action='store_true',
                        help=f'perform extraction with the {model_id} model (otherwise, only the prompt is created)')
    parser.add_argument('-n', '--num_examples', type=int, default=5,
                        help='number of examples to process from the MATH dataset')
    args = parser.parse_args()

    if args.extract:
        with open('HF_TOKEN', 'r') as file:
            hf_token = file.read().strip()

        pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            token=hf_token,
            device_map="auto",
        )

        terminators = [
            pipeline.tokenizer.eos_token_id,
            pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

    else:
        pipeline = None
        terminators = None

    input_path = "data/filtered_math_prm_test_2.jsonl"
    data = load_jsonl(input_path)

    for i, x in enumerate(data):
        print(f'\n=== Example {i} ===\n')
        messages = [
            {
                "role": "system",
                "content": "You are a world-class mathematician. You will be given a math problem and a solution. "
                           "Using your extensive knowledge of mathematics, you must go through the solution and "
                           "annotate parts which can be extracted as lemmas/tactics/heuristics of independent interest "
                           "that may be useful for solving other math problems. "
                           "Enclose the full statement of each lemma in the <lemma>LEMMA_STATEMENT</lemma> tag. "
                           "If a corresponding proof is available, enclose the proof subsequently in "
                           "<proof>PROOF</proof>. The proof must not reference elements of the problem that are not "
                           "present in the lemma's statement.\n\n"
                           "The following is an example.\n\n"
                           "Problem:\n"
                           "What is the 2003rd term of the sequence of odd numbers 1, 3, 5, 7, $\\dots$?\n\n"
                           "Solution:\n"
                           "The sequence of odd numbers 1, 3, 5, 7, and so on, is an arithmetic sequence, "
                           "with common difference 2.  Therefore, the $2003^{\\text{rd}}$ term is "
                           "$1+2002\\cdot2=\\boxed{4005}$.\n\n"
                           "Extracted lemmas:\n"
                           "<lemma>The sequence of odd natural numbers is an arithmetic sequence with common difference 2."
                           "</lemma>\n"
                           "<proof>The difference between two consecutive odd numbers, such as $3-1$ or $5-3$, is "
                           "always equal to 2.</proof>\n"
                           "<lemma>The $n$-th term of an arithmetic sequence with common difference $d$ is equal to "
                           "$a_1 + (n-1)d$, where $a_1$ is the first term.</lemma>\n"
                           "<proof>The lemma can be proved by induction on $n$, with base case $n=1$ being trivial. "
                           "For the induction step, the $n$-th term $a_n$ is equal to $a_{n-1} + d = (n-2)d + d = (n-1)d$."
                           "</proof>"},
            {
                "role": "user",
                "content": f"Problem:\n{x[PROBLEM_KEY_NAME]}\n\nSolution:\n{x[SOLUTION_KEY_NAME]}",
            },
        ]

        if args.extract:
            print(messages[-1]['content'])

            # Perform extraction using the LLM
            outputs = pipeline(
                messages,
                max_new_tokens=1024,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            )

            res = outputs[0]["generated_text"][-1]['content']

            print(res)

        else:
            # Just print the prompt
            print('\n\n'.join(y["content"] for y in messages))

        if args.num_examples is not None and i == args.num_examples - 1:
            break


if __name__ == '__main__':
    main()
