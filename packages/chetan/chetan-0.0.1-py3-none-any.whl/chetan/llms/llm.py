import os

import instructor
from pydantic import BaseModel
from chetan.core.Context import Context
from enum import Enum


class Provider(Enum):
    openai = "openai"
    anthropic = "anthropic"
    cohere = "cohere"
    groq = "groq"
    litellm = "litellm"
    mistral = "mistral"
    vertexai = "vertexai"
    other = "other"


class LLM:
    Provider: Provider
    Configuration: dict
    Client: any

    def __init__(self) -> None:
        raise NotImplementedError(
            "This is an abstract class and cannot be instantiated."
        )

    def get_structure(self, format: BaseModel, prompt: str) -> instructor.Instructor:
        """
        Get the instructor for the LLM provider.
        """
        pass

    def generate(self, context: Context | str) -> str:
        """
        Generate text based on the given context.
        """
        pass

    async def generate_async(self, context: Context | str) -> str:
        """
        Generate text asynchronously based on the given context.
        """
        pass
