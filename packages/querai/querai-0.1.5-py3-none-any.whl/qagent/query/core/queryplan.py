from typing import List

from pydantic import BaseModel

from qagent.query.core.llmprompt import LLMPrompt
from qagent.query.core.transition import Transition


class QueryPlan(BaseModel):
    prompts: List[LLMPrompt]
    transitions: List[Transition] = []
