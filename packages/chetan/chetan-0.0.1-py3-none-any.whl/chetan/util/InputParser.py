from typing import List
from pydantic import BaseModel
from chetan.core.Prompt import Prompt
from typing import Any, List, Dict, Union


class InputParser:
    def convert(self, obj: Any) -> str:
        """
        Recursively converts the object into a string representation.
        """
        if isinstance(obj, Prompt):
            return obj.prompt
        elif isinstance(obj, BaseModel):
            return self._convert_pydantic(obj)
        elif isinstance(obj, dict):
            return self._convert_dict(obj)
        elif isinstance(obj, list):
            return self._convert_list(obj)
        elif isinstance(obj, str):
            return f'"{obj}"'  # Quoting strings for clarity
        elif isinstance(obj, (int, float, bool)):
            return str(obj)  # Direct conversion for int, float, and bool
        elif obj is None:
            return "null"  # Null for NoneType
        else:
            return f'"{repr(obj)}"'  # Fallback for other types, wrapped in quotes

    def _convert_pydantic(self, model: BaseModel) -> str:
        """
        Converts a Pydantic model to a string representation.
        """
        return model.model_dump_json()

    def _convert_dict(self, obj: Dict[Any, Any]) -> str:
        """
        Converts a dictionary to a string representation.
        """
        items = [f"{self.convert(k)}: {self.convert(v)}" for k, v in obj.items()]
        return f"{{{', '.join(items)}}}"

    def _convert_list(self, obj: List[Any]) -> str:
        """
        Converts a list to a string representation.
        """
        items = [self.convert(item) for item in obj]
        return f"[{', '.join(items)}]"
