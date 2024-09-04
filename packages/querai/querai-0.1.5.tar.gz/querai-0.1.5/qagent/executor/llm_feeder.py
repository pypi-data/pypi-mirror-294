from functools import partial

from metastruct.validators.item_seq_validator import ErrEnum
from tenacity import RetryError, retry, stop_after_attempt, wait_fixed

from qagent.executor.llm_response import LLMResponse
from qagent.executor.response_to_data_binding import bind_to_data
from qagent.executor.response_validator import validate_json_response
from qagent.llms.base_lm import BaseLLM
from qagent.prompts.sys.error_prompts import Prompts
from qagent.query.core.llmprompt import LLMPrompt


def _select_retry_prompt(status: ErrEnum) -> str:
    if status == ErrEnum.BAD_RESP:
        prompt = Prompts.correct_json
    elif status == ErrEnum.BAD_SCHEMA:
        prompt = Prompts.correct_struct
    else:
        raise Exception(f"Invalid error code {status}!")
    return prompt


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(0.5),
    retry_error_callback=lambda x: None
)
def ask_again(
    status: ErrEnum,
    llm: BaseLLM,
    resp_validator: callable
) -> LLMResponse:
    """Function to reask the question."""
    prompt = _select_retry_prompt(status)
    resp = llm.generate(prompt)
    err = resp_validator(resp)
    assert err != ErrEnum.NO_ERR
    return LLMResponse(resp, err)


def ask(
    llm: BaseLLM,
    prompt: LLMPrompt
) -> LLMResponse:
    """Main function to ask a question.

    Parameters
    ----------
    llm : LLM
        _description_
    prompt : str
        _description_
    resp_constructor : Type
        _description_
    reprompt : str, optional
        _description_, by default ""

    Returns
    -------
    _type_
        _description_
    """
    # print(f"\n{'='*20}\nRun prompt {prompt.pid}")
    resp = llm.generate(prompt.text)
    resp_validator = partial(
        validate_json_response,
        response_type=prompt.response_type,
        constructor=prompt.object_constructor,
        options=prompt.choices
    )
    status = resp_validator(resp)
    if status == ErrEnum.NO_ERR:
        resp = LLMResponse(resp, ErrEnum.NO_ERR)
    else:
        try:
            resp = ask_again(status, llm, resp_validator)
        except RetryError:
            print("Maximum retry FAILED")
            resp = LLMResponse(None, ErrEnum.MAX_ATTEMPTS_REACHED)
    if resp.err == ErrEnum.NO_ERR:
        resp.data = bind_to_data(
            resp.resp,
            prompt.response_type,
            prompt.object_constructor
        )
    # print(f"FINALRESP= {resp.err} | {resp.resp} | data={resp.data}")
    return resp
