from requests import Session

from .resources import AuthenticationResource, ItemsResource


class Api:
    def __init__(self, token: str):
        self.session = Session()
        self.session.headers["Authorization"] = f"Bearer {token}"

        self._base_url = "http://localhost:3000/api"

        self.authentication = AuthenticationResource(self)
        self.items = ItemsResource(self)
