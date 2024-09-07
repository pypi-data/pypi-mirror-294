from typer import Typer

from .auth import auth_typer
from .items import items_typer

api_typer = Typer()
api_typer.add_typer(auth_typer, name="auth")
api_typer.add_typer(items_typer, name="items")
