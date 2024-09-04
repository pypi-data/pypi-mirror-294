from pydantic import BaseModel, ValidationError
from instructor.exceptions import InstructorRetryException

from chetan.agent.AgentCore import AgentCore
from chetan.llms.llm import LLM


class MitraAgentCore(AgentCore):
    """The official, opinionated, robust implementation of the AgentCore."""

    def __init__(self, llm: LLM):
        super().__init__(llm)

    def instruct(self, instruction: str) -> str | tuple[str, str]:
        try:
            return self.llm.generate_async(instruction)
        except InstructorRetryException as e:
            return self.respond(
                f"Sorry, there was an error with the property details you provided: {str(e)}",
                e,
            )

    def instruct_structured(
        self, instruction: str, format: BaseModel
    ) -> BaseModel | tuple[str, str]:
        try:
            return self.llm.get_structure(format, f"{instruction}")
        except InstructorRetryException as e:
            return self.respond(
                f"Sorry, there was an error with the property details you provided: {str(e)}"
            )
        except ValidationError as e:
            return self.respond(
                f"Validation error in the provided details: {str(e)}. Could you please clarify your requirements?"
            )

        except Exception as e:
            return self.respond(f"An error occurred: {str(e)}. Please try again.")

    def respond(self, response: str) -> str:
        return response

    # def think(self, prompt: str) -> Decision:
    #     return Decision(prompt)

    # def decide(self, prompt: str, options: List[BaseModel]) -> BaseModel:
    #     return options[0]

    # def validate(self, decision: Decision) -> bool:
    #     return True

    # def learn(self, context: Context):
    #     pass
