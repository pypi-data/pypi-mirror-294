from typing import Type

from qagent.executor.base_executor import QueryPlanExecutorBase
from qagent.executor.llm_feeder import ask
from qagent.llms import BaseLLM, OpenAILM
from qagent.query import to_query_plan_for_one


class SimpleSingularExecutor(QueryPlanExecutorBase):
    def __init__(
        self,
        prompt: str,
        response_type: str,
        choices: list = None,
        object_constructor: Type = None,
        llm: BaseLLM = None
    ):
        super().__init__(
            plan=to_query_plan_for_one(
                template=prompt,
                response_type=response_type,
                choices=choices,
                object_constructor=object_constructor
            ),
            llm=llm or OpenAILM()
        )

    def morph(
        self,
        prompt: str,
        object_constructor: Type,
        resp_type: str = "object"
    ):
        """Use different (Retarget) prompt and object_constructor."""
        self.plan = to_query_plan_for_one(
            template=prompt,
            response_type=resp_type,
            object_constructor=object_constructor
        )

    def execute(
        self,
        **kwargs
    ):
        prompt = self.plan.prompts[0]
        prompt.text = prompt.template.format(**kwargs)
        resp = ask(self.llm, prompt)
        return resp
