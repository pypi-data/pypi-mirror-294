from enum import Enum

from pydantic import BaseModel


class ConditionEnum(Enum):
    EQUAL = "eq"


class TransitionCondition(BaseModel):
    """Condition for a transition."""

    type: ConditionEnum
    arg: str

    def __str__(self):
        return f"({self.type} {self.arg})"


class Transition(BaseModel):
    """Transition between two prompts with a condition."""

    source: str
    """The source prompt id."""
    target: str
    """The target prompt id."""
    condition: TransitionCondition = None
    """If None, then transition is unconditional."""

    def __str__(self):
        return f"Transition from {self.source} to {self.target}"
