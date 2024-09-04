import json
from typing import Set, Type

from metastruct.basetypes import ErrEnum
from metastruct.validators import (is_dict_of_list, is_list_of_str,
                                   is_valid_choice, is_valid_item)

from qagent.query.core.response_type import ResponseTypeEnum


def validate_response(
    response: str,
    response_type: ResponseTypeEnum,
    constructor: Type = None,
    options: Set = None
) -> ErrEnum:
    """Function to validate the response.

    Parameters
    ----------
    response : str
        _description_
    constructor : Type, optional
        Can be a specific object type dynamically passed in,
        to enable arbitrary object validation, by default None
    """
    status = ErrEnum.NO_ERR
    if response_type == ResponseTypeEnum.CHOICES:
        status = is_valid_choice(response, options)
    elif response_type == ResponseTypeEnum.LIST:
        status = all(isinstance(v, str) for v in response)
    elif response_type == ResponseTypeEnum.OBJECT:
        status = is_valid_item(response, constructor)
    elif response_type == ResponseTypeEnum.DICTOFLIST:
        status = is_dict_of_list(response)
    else:
        raise ValueError(f"Invalid response type {response_type}!")

    # Cast back to `ErrEnum`
    status = ErrEnum.NO_ERR if status else ErrEnum.BAD_RESP

    return status


def validate_json_response(
    response: str,
    response_type: ResponseTypeEnum,
    constructor: Type = None,
    options: Set = None
) -> ErrEnum:
    """Validate the response when LLM returns a `json_object`."""
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        return ErrEnum.BAD_RESP

    if response_type == ResponseTypeEnum.CHOICES:
        data = next(iter(data.values()))
    elif response_type == ResponseTypeEnum.LIST:
        data = next(iter(data.values()))
    else:
        data = data

    status = validate_response(
        response=data, response_type=response_type, constructor=constructor, options=options)
    return status
