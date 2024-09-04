from typing import List, Optional, Type

from pydantic import BaseModel, field_validator

from qagent.query.core.response_type import ResponseTypeEnum

DIR_PROMPT_LIB = "qagent/prompts/libs"


class LLMPrompt(BaseModel):
    pid: str
    """ID of prompt, either set by user or auto-generated"""
    template: str
    """Prompt template to be filled in."""
    response_type: ResponseTypeEnum
    """`kind` of response expected from the user. """
    choices: Optional[List] = None
    """List of choices if response_type is CHOICES."""
    object_constructor: Optional[Type] = None
    """Constructor for validation, if response_type is OBJECT."""
    metadata: dict = {}
    example: str = None
    sysprompt: str = ""
    """System prompt."""
    text: str = ""
    """Prompt text."""

    def model_post_init(self, __context):
        # Get prompt from file if `text` starts with `@`
        if self.template.startswith("@"):
            promptfile = f"{DIR_PROMPT_LIB}/{self.template[1:]}.txt"
            with open(promptfile) as fh:
                self.template = fh.read().strip()
        return super().model_post_init(__context)

    @field_validator("text", mode="after")
    @classmethod
    def validate_prompt_text(cls, value):
        if not value:
            raise ValueError("Prompt cannot be empty!")
        return value
