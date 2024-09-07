from typing import Annotated

from typer import Option, Typer

from ...common import _api

items_typer = Typer()

Id = Annotated[int, Option()]


@items_typer.command("create")
def create(key: Annotated[str, Option()], value: Annotated[str, Option()]):
    return _api.items.create(key, value=value)


@items_typer.command("find-all")
def find_all():
    items = _api.items.find_all()

    print(items)


@items_typer.command("delete")
def delete(id_: Id):
    return _api.items.delete(id_)


@items_typer.command("find-one")
def find_one(id_: Id):
    item = _api.items.find_one(id_)

    print(item)
