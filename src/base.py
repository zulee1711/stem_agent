"""
Baseline agent: vanilla gpt-4o-mini with NO specialization.
Intentionally weaker model so the evolved agent has room to improve
"""

import os
from http.client import responses

from openai import OpenAI

#%%
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

BASELINE_SYSTEM = """
You are a Python programmer. When given a coding problem, write a correct Python solution.
Rules:
- Write ONLY the solve() function and any helpers it needs
- Use only standard library
- Return only raw Python code, no explanations
"""

#%%
def base_solve(problem_description: str) -> str:
    """
    Call gpt-4o-mini with no scaffolding
    :return: raw Python code string
    """
    default_model = "gpt-4o-mini"
    response = client.chat.completions.create(
        model=default_model,
        messages=[
            {"role": "system", "content": BASELINE_SYSTEM},
            {"role": "user", "content": problem_description}
        ],
        temperature = 0.2,
        max_tokens = 800,
    )
    return response.choices[0].message.content