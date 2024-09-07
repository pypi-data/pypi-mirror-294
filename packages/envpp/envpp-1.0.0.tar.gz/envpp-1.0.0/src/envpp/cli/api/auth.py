from typing import Annotated

from typer import Option, Typer

from ...common import _api

auth_typer = Typer()

Email = Annotated[str, Option(prompt="Email")]
Password = Annotated[str, Option(prompt="Password")]


@auth_typer.command("sign-in")
def sign_in_callback(email: Email, password: Password):
    sign = _api.authentication.sign_in(email, password=password)

    print(f"Token: {sign.token}")


@auth_typer.command("sign-up")
def sign_up_callback(email: Email, password: Password):
    sign = _api.authentication.sign_up(email, password=password)

    print(f"Token: {sign.token}")
