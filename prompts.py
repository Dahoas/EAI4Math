prompts = dict(
    lemma_extraction="""\
You are a top maths student. You are shown the following question + answer pair
Problem:
{problem}
Solution:
{solution}
Using your extensive knowledge of mathematics, you must go through the solution and 
annotate sub-parts which can be extracted as tactics/lemmas of independent interest that may
be useful for solving other math questions. Enclose each extracted lemma in the json format
<lemma>
{{
    'statement': statement of lemma,
    'proof': proof of lemma,
    'description': description of when lemma is useful,
}}
</lemma>
""",
    lemma_requests="""\
You are a top maths student. You are trying to solve the following question:
Problem:
{problem}
You are tasked with brainstorming five descriptions of any lemmas that may be useful 
for solving the problem. Write this in the format:
**Lemma Description 1:**
Description of Lemma
**Lemma Description 2:**
Description of Lemma
...
""",
    retrieved_lemma_math_solve="""\
You are a top maths student. Your goal is to solve the following maths problem:
{problem}
You may find the following lemmas useful:
{lemmas}
"""
)