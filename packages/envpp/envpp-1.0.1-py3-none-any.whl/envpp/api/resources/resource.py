from typing import TYPE_CHECKING, TypeVar

from msgspec.json import decode

from ..structs import ErrorStruct

if TYPE_CHECKING:
    from .. import Api


T = TypeVar("T")


class Resource:
    def __init__(self, api: "Api"):
        self.api = api

    def request(
        self,
        method: str,
        endpoint: str,
        type_: type[T],
        data: dict[str, str] | None = None,
    ) -> T:
        response = self.api.session.request(
            method, f"{self.api._base_url}/{endpoint}", data=data
        )

        if response.status_code != 200:
            error = decode(response.text, type=ErrorStruct)

            raise Exception(error.message)

        return decode(response.text, type=type_)
