from chetan.agent.AgentCore import AgentCore


class AgentBody:
    def __init__(self):
        pass

    def prompt(self, prompt: str, agent: AgentCore) -> str:
        raise NotImplementedError(
            "The prompt method must be implemented by the subclass."
        )
