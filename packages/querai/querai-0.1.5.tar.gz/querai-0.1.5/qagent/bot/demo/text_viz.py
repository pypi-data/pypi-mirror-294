from typing import List

from pydantic import BaseModel, Field

from qagent.executor.base_executor import QueryPlanExecutorBase
from qagent.llms import OpenAILM


class GraphNode(BaseModel):
    id: int
    label: str
    type: str = Field(default='Node')


class GraphEdge(BaseModel):
    source: int
    target: int
    label: str


class Network(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class GraphNodeFromTable(BaseModel):
    type: str
    columns: List[str]


class GraphEdgeFromTable(BaseModel):
    source: str
    target: str


class GraphConfigFromTable(BaseModel):
    nodetypes: List[GraphNodeFromTable]
    edges: List[GraphEdgeFromTable]


class TextToVisualExecutor(QueryPlanExecutorBase):

    def __init__(self, planfile: str = None, plantext: str = None):
        super().__init__(planfile=planfile, plantext=plantext, llm=OpenAILM())

    # --- demo ---
    # Create structured information from raw text
    def tie_to_object(self) -> None:
        for prompt in self._query_plan.prompts:
            if prompt.pid == "a03":
                prompt.object_constructor = Network
            elif prompt.pid == "a05":
                prompt.object_constructor = GraphConfigFromTable
