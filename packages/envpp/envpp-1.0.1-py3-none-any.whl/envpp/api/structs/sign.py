from msgspec import Struct


class SignStruct(Struct):
    token: str
