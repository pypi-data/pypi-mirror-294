from typing import List
from typing_extensions import deprecated
from chetan.agent.AgentResponse import AgentResponse
from chetan.core.Context import Context
from chetan.core.Decision import Decision
from chetan.knowledge.Knowledgebase import KnowledgeBase
from pydantic import BaseModel

from chetan.core.Prompt import PROMPT_DECIDE_TASK, PROMPT_UNDERSTAND, Prompt
from chetan.llms.llm import LLM
from chetan.recipe.task.Task import Task

import instructor


@deprecated("You should use Agent()")
class AgentExecutor:

    def __init__(
        self, llm: LLM, knowledgebase: KnowledgeBase, apps: List[str], tasks: List[Task]
    ):

        self.llm = llm
        self.knowledgebase = knowledgebase
        self.apps = apps
        self.tasks = tasks

        # self.memory = tuple(Context(), {})

    # TODO: implement think()
    async def think(self, task: str) -> Decision:
        """
        Process the task and generate a thought process.
        """

        thought = await self.instruct(task)

        # More complex logic goes here
        # return thought_process

    # TODO: implement decicde()
    async def decide(self, prompt: str, options: List[BaseModel]) -> BaseModel:
        """
        Make a decision based on the thought process and available options.
        """
        # Example of decision-making logic
        decision = options[
            0
        ]  # This is a simplified example; more logic would be added here
        return decision

    # TODO: implement validate()
    async def validate(self, decision: Decision) -> bool:
        """
        Validate the decision made by the agent.
        """
        # Example of validation logic
        return decision in self.apps

    def instruct(self, instruction: str) -> str:
        """
        Instructs the llm, expecting a string output.
        """
        return self.llm.generate_async(instruction)

    def instruct_structured(self, instruction: str, format: BaseModel) -> BaseModel:
        """
        Instructs the llm, expecting a structured output.
        """
        return self.llm.get_structure(format, instruction)

    async def learn(self, context: Context):
        """
        Learn new knowledge from a specific context, storing in the knowledgebase.
        """
        pass

    # TODO: implement safety_check()
    async def safety_check(self, options: Decision) -> bool:
        """
        Perform a safety check on the decision made by the agent.
        """
        # Example of safety check logic
        return True

    async def invoke(self, prompt: Prompt | str) -> AgentResponse:
        """
        Invoke the agent to perform a task.
        """

        pass
