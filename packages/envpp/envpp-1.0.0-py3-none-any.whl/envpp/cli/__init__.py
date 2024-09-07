from typing import Annotated

from typer import Option, Typer

from ..common import _api, path
from .api import api_typer

typer = Typer()
typer.add_typer(api_typer, name="api")


@typer.command("generate")
def generate_callback():
    items = _api.items.find_all()
    items_keys = ", ".join([f'"{item.key}"' for item in items])
    items_keys_and_ids = ", ".join([f'"{item.key}":{item.id_}' for item in items])

    item_python_file = path / "_item.py"
    item_template_file = path / "_item.template"

    item_python_file.write_text(
        item_template_file.read_text()
        .replace("{items_keys}", items_keys)
        .replace("{items_keys_and_ids}", items_keys_and_ids)
    )


@typer.command("set-token")
def set_token_callback(token: Annotated[str, Option()]):
    email_file = path / "token.txt"
    email_file.write_text(token)
