import instructor
from openai import OpenAI
from pydantic import BaseModel
from chetan.core.Context import Context
from chetan.llms.llm import LLM, Provider


class Ollama(LLM):
    Provider = Provider.openai
    Configuration = {"model": "llama3.1:8b-instruct-q5_K_S"}

    def __init__(self) -> None:
        pass

    def get_structure(
        self, format: BaseModel, prompt: str
    ) -> str:  # instructor.Instructor:
        """
        Get the instructor for the LLM provider.
        """
        inst = instructor.from_openai(
            OpenAI(
                base_url="http://192.168.10.179:11434/v1",
                api_key="ollama",  # required, but unused
            ),
            instructor.Mode.JSON,
        )

        conf = self.Configuration
        conf["response_model"] = format
        conf["messages"] = [{"role": "user", "content": prompt}]

        return inst.create(**self.Configuration)

    async def generate_async(self, context: Context | str) -> str:
        """
        Generate text asynchronously based on the given prompt. Contextless.
        """
        inst = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",  # required, but unused
        )

        conf = self.Configuration
        # conf["stream"] = True
        conf["messages"] = [{"role": "user", "content": context}]

        return inst.chat.completions.create(**self.Configuration)

        # for chunk in stream:
        # if chunk.choices[0].delta.content != None:
        # print(chunk.choices[0].delta.content, end="")
        # print()
