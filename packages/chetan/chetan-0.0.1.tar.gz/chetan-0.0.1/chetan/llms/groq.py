import instructor
from pydantic import BaseModel
from chetan.core.Context import Context
from chetan.llms.llm import LLM, Provider

from groq import Groq as Groq_LLM


class Groq(LLM):
    Provider = Provider.groq
    Configuration = {"model": "llama3-8b-8192"}

    def __init__(self) -> None:
        pass

    def get_structure(
        self, format: BaseModel, prompt: str
    ) -> str:  # instructor.Instructor:
        """
        Get the instructor for the LLM provider.
        """
        inst = instructor.from_groq(Groq_LLM())

        conf = self.Configuration
        conf["response_model"] = format
        conf["messages"] = [{"role": "user", "content": prompt}]

        return inst.create(**self.Configuration)

    async def generate_async(self, context: Context | str) -> str:
        """
        Generate text asynchronously based on the given prompt. Contextless.
        """
        inst = Groq_LLM()

        conf = self.Configuration
        # conf["stream"] = True
        conf["messages"] = [{"role": "user", "content": context}]

        return inst.chat.completions.create(**self.Configuration)

        # for chunk in stream:
        # if chunk.choices[0].delta.content != None:
        # print(chunk.choices[0].delta.content, end="")
        # print()
