from ._item import Item, items
from .common import _api


class Envpp:
    def __init__(self) -> None:
        pass

    def __getitem__(self, key: Item) -> str:
        return _api.items.find_one(items[key]).value
