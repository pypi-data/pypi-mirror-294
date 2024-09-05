from hackathon.helpers import get_completion_from_prompt


def evaluate(answer):

    prompt = f"""Please evaluate if the following answer is correct.

Answer: <answer>{answer}</answer>

The solution should contain the following two pieces of insight:
- Customers in the United States (USA) are very unsatisfied compared to the other countries. Alternatively, the United States has the least satisfied customers.
- Customers in China are the most satisfied.

How many of the insights did the answer contain? Reply ONLY with integer.
"""
    return f"Your answer contains {int(get_completion_from_prompt(prompt))} of the 2 desired insights."
