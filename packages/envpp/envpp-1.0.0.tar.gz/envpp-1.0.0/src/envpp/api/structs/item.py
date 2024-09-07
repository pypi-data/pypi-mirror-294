from msgspec import Struct, field


class ItemStruct(Struct):
    id_: int = field(name="id")
    user_id: int = field(name="userId")
    key: str
    value: str
