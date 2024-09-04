class Prompt:
    def __init__(self, prompt):
        self.prompt = prompt

    def get_for_agent(self) -> str:
        return self.prompt

PROMPT_UNDERSTAND = """
I need to understand the given prompt from the user.
{prompt}
"""

PROMPT_DECIDE_TASK = """
To fulfill the user's request, I need to pick the appropriate task body for the given prompt.

{prompt}
"""
