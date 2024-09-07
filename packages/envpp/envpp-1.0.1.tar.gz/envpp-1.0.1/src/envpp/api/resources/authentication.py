from ..structs import SignStruct
from .resource import Resource


class AuthenticationResource(Resource):
    def sign_in(self, email: str, password: str) -> SignStruct:
        return self.request(
            "POST",
            endpoint="sign-in",
            type_=SignStruct,
            data={"email": email, "password": password},
        )

    def sign_up(self, email: str, password: str) -> SignStruct:
        return self.request(
            "POST",
            endpoint="sign-up",
            type_=SignStruct,
            data={"email": email, "password": password},
        )
