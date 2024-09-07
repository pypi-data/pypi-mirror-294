from typing import Literal

from msgspec import Struct


class ErrorStruct(Struct):
    name: Literal["Error"]
    message: str
