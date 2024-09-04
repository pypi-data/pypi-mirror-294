from chetan.agent.AgentBody import AgentBody
from chetan.agent.AgentCore import AgentCore
from chetan.agent.AgentResponse import AgentResponse
from chetan.core.Prompt import PROMPT_DECIDE_TASK, PROMPT_UNDERSTAND


class MitraAgentBody(AgentBody):
    """The official, opinionated, robust implementation of the AgentBody."""

    def __init__(self):
        pass

    def prompt(self, prompt: str, agent: AgentCore) -> AgentResponse:
        # TODO: implement Agent v1

        # ! Understand the task
        AGENT_understanding = agent.think(
            task=PROMPT_UNDERSTAND.format(prompt=prompt.get_for_agent()),
        )

        AGENT_understood = agent.validate(AGENT_understanding)

        if not AGENT_understood:
            return AgentResponse(
                success=False, message="The agent could not understand the task."
            )

        # ! Perform risk/ethical assesment

        AGENT_risk = agent.safety_check(AGENT_understanding)

        if not AGENT_risk:
            return AgentResponse(
                success=False,
                message="The agent could not perform the task due to safety/ethical concerns.",
            )

        # ! Decide the appropriate task body for the task

        AGENT_task = agent.decide(prompt=PROMPT_DECIDE_TASK, options=self.tasks)
