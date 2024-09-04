from typing import List
from chetan.agent.AgentCore import AgentCore
from chetan.agent.AgentBody import AgentBody
from chetan.knowledge.Knowledgebase import KnowledgeBase
from chetan.recipe.MitraAgentBody import MitraAgentBody
from chetan.recipe.MitraAgentCore import MitraAgentCore
from chetan.llms.llm import LLM
from chetan.llms.openai import OpenAI


class Agent:
    def __init__(
        self,
        body: AgentBody = MitraAgentBody(),
        core: AgentCore = MitraAgentCore,
        llm: LLM = OpenAI(),
        knowledgebase: KnowledgeBase = None,
        apps: List[str] = [],
    ):
        self.body = body
        self.llm = llm
        self.core = core(self.llm)
        self.knowledgebase = knowledgebase
        self.apps = apps

    def invoke(self, prompt: str):
        return self.body.prompt(prompt, self.core)

    def interact(self):
        while True:
            prompt = input("You: ")
            # try:
            response = self.invoke(prompt)
            print(f"Bot: {response}")
            # except Exception as e:
            #     print(f"Error: {e}")
            #     continue
