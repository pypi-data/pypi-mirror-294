from typing import List
from pydantic import BaseModel

from chetan.core.Context import Context
from chetan.core.Decision import Decision
from chetan.llms.llm import LLM


class AgentCore:
    def __init__(self, llm: LLM):
        self.llm = llm
        pass

    # REGION: Primitives
    def instruct(self, instruction: str) -> str:
        """Instruct the agent with a given `instruction` and return a response.

        Args:
            instruction (str): The instruction to give to the agent.

        Raises:
            NotImplementedError: This method must be implemented by an AgentCore subclass.

        Returns:
            str: The response from the agent.
        """
        raise NotImplementedError()

    def instruct_structured(self, instruction: str, format: BaseModel) -> BaseModel:
        """Instruct the agent with a given `instruction` and return a structured response.

        Args:
            instruction (str): The instruction to give to the agent.
            format (BaseModel): The format of the response.

        Raises:
            NotImplementedError: This method must be implemented by an AgentCore subclass.

        Returns:
            BaseModel: The structured response from the agent.
        """
        raise NotImplementedError()

    # TODO: implement query
    # TODO: implement store
    # TODO: implement evaluate

    # ENDREGION

    def think(self, prompt: str) -> Decision:
        """Think based on the given `prompt` and yield a `Decision`.

        Args:
            prompt (str): The user prompt.

        Raises:
            NotImplementedError: This method must be implemented by an AgentCore subclass.

        Returns:
            Decision: The decision made by the agent.
        """
        raise NotImplementedError()

    def decide(self, prompt: str, options: List[BaseModel]) -> BaseModel:
        """Chooses an option from a list of options based on the given `prompt`.

        Args:
            prompt (str): The user prompt.
            options (List[BaseModel]): The list of options to choose from.

        Raises:
            NotImplementedError: This method must be implemented by an AgentCore subclass.

        Returns:
            BaseModel: The chosen option.
        """
        raise NotImplementedError()

    def validate(self, decision: Decision) -> bool:
        """Validates a given `decision`.

        Args:
            decision (Decision): The decision to validate.

        Raises:
            NotImplementedError: This method must be implemented by an AgentCore subclass.

        Returns:
            bool: `True` if the decision is valid, `False` otherwise.
        """
        raise NotImplementedError()

    def learn(self, context: Context):
        """Learns new knowledge from a specific `context`, storing it in the knowledgebase.

        Args:
            context (Context): The context to learn from.

        Raises:
            NotImplementedError: This method must be implemented by an AgentCore subclass.
        """
        raise NotImplementedError()

    def respond(self, response: str) -> str:
        raise NotImplementedError()

    # TODO: implement adapt
    # TODO: implement analyze
    # TODO: implement collaborate
    # TODO: implement plan
    # TODO: implement reflect
