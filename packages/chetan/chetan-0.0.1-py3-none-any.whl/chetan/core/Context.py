from typing import List, Union
from chetan.agent.AgentResponse import AgentResponse
from chetan.core.Prompt import Prompt


class Context:
    def __init__(self, agent_output: AgentResponse, prompt: Prompt):
        self.agent_output = agent_output
        self.prompt = prompt

        # Initialize a list to store the context items
        self.context_items = []

    def push(self, item: Union[Prompt, AgentResponse]):
        # Add the item to the context list
        self.context_items.append(item)

    def get_for_agent(self) -> List[Union[Prompt, AgentResponse]]:
        # Return the context items, potentially filtering based on agent's needs
        return self.context_items

    def search_context(self, query: str) -> Union[Prompt, AgentResponse, None]:
        # Example method to search context for a specific item
        for item in reversed(
            self.context_items
        ):  # Search in reverse order for the latest context
            if isinstance(item, Prompt) and query in item.content:
                return item
            elif isinstance(item, AgentResponse) and query in item.response:
                return item
        return None

    def clear_context(self):
        # Method to clear the context list if needed
        self.context_items.clear()
