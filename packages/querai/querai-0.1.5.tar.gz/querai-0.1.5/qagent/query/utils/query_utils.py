from typing import Type

from qagent.query.core import LLMPrompt, QueryPlan


def to_query_plan_for_one(
    template: str,
    response_type: str,
    choices: list = None,
    object_constructor: Type = None,
    default_prompt_id: str = "random1"
) -> QueryPlan:
    """Return a query plan for a single prompt."""
    return QueryPlan(
        prompts=[
            LLMPrompt(
                pid=default_prompt_id,
                template=template,
                response_type=response_type,
                choices=choices,
                object_constructor=object_constructor
            )
        ],
        transitions=[]
    )
