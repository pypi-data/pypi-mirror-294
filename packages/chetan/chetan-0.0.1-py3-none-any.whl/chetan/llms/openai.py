import instructor
from pydantic import BaseModel
from chetan.core.Context import Context
from chetan.llms.llm import LLM, Provider

from openai import AzureOpenAI as OpenAI_LLM


class OpenAI(LLM):
    """
    OpenAI LLM provider for chetan.
    """

    Provider = Provider.openai
    Configuration = {"model": "gpt-4o-mini"}

    def __init__(self) -> None:
        pass

    def get_structure(self, format: BaseModel, prompt: str) -> instructor.Instructor:
        """
        Get the instructor for the LLM provider.
        """
        inst = instructor.from_openai(
            OpenAI_LLM(
                azure_endpoint="https://chetan-gpt.openai.azure.com",
                api_version="2024-02-15-preview",
                api_key="cd0d022f3b2843109ba3c8e780f506db",
            )
        )

        conf = self.Configuration
        conf["response_model"] = format
        conf["messages"] = [{"role": "user", "content": prompt}]

        return inst.create(**self.Configuration)

    def generate_async(self, context: Context | str) -> str:
        """
        Generate text asynchronously based on the given prompt. Contextless.
        """
        inst = OpenAI_LLM(
            azure_endpoint="https://chetan-gpt.openai.azure.com/",
            api_version="2024-02-15-preview",
            api_key="cd0d022f3b2843109ba3c8e780f506db",
        )

        conf = self.Configuration
        # conf["stream"] = True
        conf["messages"] = [{"role": "user", "content": context}]

        return inst.chat.completions.create(**self.Configuration)

        # for chunk in stream:
        # if chunk.choices[0].delta.content != None:
        # print(chunk.choices[0].delta.content, end="")
        # print()
