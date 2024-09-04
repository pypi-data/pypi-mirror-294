from enum import Enum


class ResponseTypeEnum(str, Enum):
    CHOICES = "choice"
    OBJECT = "object"
    LIST = "list"
    DICTOFLIST = "dict-of-list"
