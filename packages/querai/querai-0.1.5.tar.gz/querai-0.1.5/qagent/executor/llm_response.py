from typing import Any

from metastruct.validators.item_seq_validator import ErrEnum


class LLMResponse:
    """Class representing the response from LLM."""

    def __init__(self, resp: str, err: ErrEnum, data: Any = None):
        self.resp = resp
        self.err = err
        self.data = data
        """Actual `data` created upon valid `resp`"""

    def __str__(self):
        return f"LLMResponse: {self.resp}\nError: {self.err}\nData: {self.data}"
