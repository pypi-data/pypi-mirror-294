import json
from typing import Optional

from qagent.query.core import QueryPlan


def read_qplan(
    plan: Optional[QueryPlan] = None,
    planfile: str = None,
    plantext: str = None
) -> QueryPlan:
    """Reads a query plan from a file."""
    assert plantext or planfile or plan
    if isinstance(plan, QueryPlan):
        return plan
    else:
        if planfile:
            with open(planfile, 'r') as f:
                qplan = json.load(f)
        else:
            qplan = json.loads(plantext)
        return QueryPlan(**qplan)
