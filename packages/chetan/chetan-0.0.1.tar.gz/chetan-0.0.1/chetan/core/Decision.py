from pydantic import BaseModel


class Decision(BaseModel):
    decision: str
    confidence: float
    outcomes: list[str]