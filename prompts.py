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
    math_solve="""\
You are a top maths student. Your goal is to solve the following maths problem:
{problem}
You should box your final answer at the end of your response in the form:
\\boxed{{FINAL_ANSWER}}""",
    library_math_solve="""\
You are a top maths student. Your goal is to solve the following maths problem:
{problem}
You may find the following lemmas useful:
{retrieved_lemmas_str}
You should box your final answer at the end of your response in the form:
\\boxed{{FINAL_ANSWER}}
""",
    lean_4_tips="""
The syntax for Lean 4 is different than that of Lean 3 - premises like "Nat.dvd_mul" and "Finset.singleton_injective" exist in Lean 4, \
the equivalent in Lean 3 is "nat.dvd_mul" and "finset.singleton_injective" which DO NOT WORK in Lean 4. \
Additionally, you cannot chain tactics into one step using ',' - this will NOT work - you can use ';' \
instead but try to avoid such usage where not necessary! When doing rewrites you MUST wrap the premise in brackets: "rw [h]". \
If you want to do multiple rewrites at once you can do something like "rw [step1, step2, step3]". \
Always predict one tactic at a time, though you can predict the "have" tactic and may supply a proof for it with tactics split by ";". \
You can provide witnesses to consecutive existential quantifiers all at once, for example 'use 1, 2, 3' but NOT as a list 'use \
[1, 2, 3]' - these are not the same things! You can introduce with "intro" everything you think you can introduce at once. \
In Lean 4, you can split apart conjunctions with "constructor" NOT "split". \
You should use the "ring" tactic to handle goals that follow from ring axioms, especially instead of doing a long series of rewrites \
or calculations. Similarly, "linarith" can be useful for solving goals involving linear arithmetic. \
Do NOT indent tactics, every new line should not have spaces to start! PLEASE use Lean 4 syntax only!
""",
    vanilla_autoformalization="""\
You are a tasked with formally proving the following statement in Lean4:
{formal_statement}\n\n
To help, you are provided the following informal statement and informal proof.
Statement:
{informal_stmt}\n\n
Proof:
{informal_proof}\n\n
Enclose your final formal proof in the environment ```lean\n...\n```
You should never use the Sorry keyword.
{lean_4_tips}
""",
    subgoal_extraction_autoformalization="""\
You are a tasked with formally proving the following statement in Lean4:
{formal_statement}\n\n
To help, you are provided the following informal statement and informal proof.
Statement:
{informal_stmt}\n\n
Proof:
{informal_proof}\n\n
Your job is to break the informal proof into a sequence of formal sub-goals that will help you prove the formal statement.
Specifically, you should generate a sub-goal lean4 statements WITHOUT proving anything.
Enclose each sub-goal statement in separate environments ```lean\n...\n```
Each lean sub-goal should be named goal_1, goal_2,...
There is no need to be extremely detailed. You should only have lean sub-goal per proof section.
You can and should use conclusions from earlier subgoals as assumptionsin later sub-goals.
"""
)