from qagent.executor.llm_feeder import ask
from qagent.llms import BaseLLM
from qagent.query.core import QueryPlan
from qagent.query.core.response_type import ResponseTypeEnum
from qagent.query.utils.read_plan import read_qplan


class QueryPlanExecutorBase:
    llm: BaseLLM

    def __init__(
        self,
        plantext: str = None,
        planfile: str = None,
        plan: QueryPlan = None,
        llm: BaseLLM = None
    ) -> None:
        self._query_plan_file = planfile
        self._query_plan_text = plantext
        self._query_plan = read_qplan(
            plan=plan, planfile=planfile, plantext=plantext)
        self.llm = llm

        self.tie_to_object()
        self._add_sysprompt()

    @property
    def planfile(self) -> str:
        return self._query_plan_file

    @planfile.setter
    def planfile(self, planfile: str) -> None:
        self._query_plan_file = planfile

    @property
    def plan(self) -> QueryPlan:
        return self._query_plan

    @plan.setter
    def plan(self, queryplan: QueryPlan) -> None:
        self._query_plan = queryplan

    def _add_sysprompt(self) -> None:
        """Add system prompt to each prompt in the plan."""
        for prompt in self.plan.prompts:
            if prompt.response_type == ResponseTypeEnum.CHOICES:
                choices = ",".join(prompt.choices)
                prompt.template += (
                    "\nJSON schema is `answer`-> <choice> "
                    "where `choice` is one of the following: "
                    f"{choices}"
                )
            elif prompt.response_type == ResponseTypeEnum.LIST:
                prompt.template += "\nYour answer's JSON schema is {{`answer`: [items]}}"

    def tie_to_object(self) -> None:
        """Associate each object prompt to a specific object.

        The child class can use this to tie to specific object like

        >>> class Person:
        >>>    pass
        >>> class MyExecutor(QueryPlanExecutorBase):
        >>>   def tie_to_object(self):
        >>>       for prompt in self._query_plan.prompts:
        >>>           if prompt.pid == "person":
        >>>               prompt.object_constructor = Person
        """
        pass

    def execute(
        self,
        user_input: str
    ):
        for _, prompt in enumerate(self.plan.prompts):
            # Tie to user input
            prompt.text = prompt.template.format(**{
                "user_input": user_input
            })
            resp = ask(self.llm, prompt)
        return resp
