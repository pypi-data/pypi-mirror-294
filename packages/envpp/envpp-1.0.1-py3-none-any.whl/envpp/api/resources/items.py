from ..structs import ItemStruct
from .resource import Resource


class ItemsResource(Resource):
    def create(self, key: str, value: str):
        self.request("POST", endpoint="items", data={"key": key, "value": value})

    def find_all(self) -> list[ItemStruct]:
        return self.request("GET", endpoint="items", type_=list[ItemStruct])

    def delete(self, id_: int):
        self.request("DELETE", endpoint=f"items/{id_}")

    def find_one(self, id_: int) -> ItemStruct:
        return self.request("GET", endpoint=f"items/{id_}", type_=ItemStruct)
