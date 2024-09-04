import json
from typing import Any, Type

from qagent.query.core.response_type import ResponseTypeEnum


def bind_to_data(
    response: str,
    response_type: ResponseTypeEnum,
    constructor: Type = None
) -> Any:
    """Create valid python data from the response.

    The LLM response is raw text, thus needs to be converted to a valid python
    data for further processing.

    More details:

    - For `LIST`, the raw text resonse of LLM may be:
    ```
    {
        "answer": ["item1", "item2"]
    }
    ```
    """
    data = json.loads(response)
    if response_type == ResponseTypeEnum.LIST:
        data = next(iter(data.values()))
    elif response_type == ResponseTypeEnum.CHOICES:
        data = next(iter(data.values()))
    elif response_type == ResponseTypeEnum.OBJECT:
        data = constructor(**data)
    else:
        data = data
    return data
