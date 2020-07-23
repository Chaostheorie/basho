#!/usr/bin/env python3

__doc__ = "Basho CLI Toolkit for management and development"
__author__ = "Cobalt <https://cobalt.rocks>"
__version__ = "0.0.1"

import click
import asyncio
from functools import wraps
from app.helper import connect


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group()
def toolkit():
    click.echo(f"Boardgame-Backend Toolkit v{__version__} by {__author__}")


@toolkit.command()
@click.option("--root", default=".", type=click.Path())
@click.option("--fast", is_flag=True, default=False, type=bool)
def format(root, fast):
    """Formats all python files in basho/ with black"""
    click.echo("Black is run against basho/")
    from black import format_file_contents, FileMode, NothingChanged
    from os import walk, path

    directory = path.join(root, "basho/")
    changes = [0, 0]

    for root, subdirs, files in walk(directory):
        for filename in files:
            file_path = path.join(root, filename)
            if file_path[-3:] != ".py":
                continue
            with open(file_path, "r") as f:
                try:
                    out = format_file_contents(f.read(), fast=fast, mode=FileMode())
                    changes[0] += 1
                    with open(file_path, "w") as f:
                        f.write(out)
                except NothingChanged:
                    changes[1] += 1

    click.echo(f"{changes[0]} changed/ {changes[1]} not changed")


@toolkit.command()
@click.option("-p", "--port", type=int, default=8000, show_default=True)
@click.option("--reload/--production", type=bool, default=True, show_default=True)
@click.option("-h", "--host", type=str, default="127.0.0.1", show_default=True)
@click.option(
    "--http",
    type=click.Choice(["auto", "httptools", "h11"], case_sensitive=False),
    default="auto",
    show_default=True,
)
@click.option(
    "--loop",
    type=click.Choice(["auto", "asyncio", "uvloop", "iocp"], case_sensitive=False),
    default="uvloop",
    show_default=True,
)
@click.option(
    "--log-level",
    type=click.Choice(
        ["critical", "error", "warning", "info", "debug", "trace"], case_sensitive=False
    ),
    default="info",
    show_default=True,
)
@click.option("--workers", type=int, default=4, show_default=True)
def devserver(port, reload, host, http, loop, workers, log_level):
    """
    Run a uvicorn instance serving app
    Options: https://www.uvicorn.org/#running-programmatically#command-line-options
    """
    from uvicorn import run

    run(
        "app:app",
        http=http,
        loop=loop,
        workers=workers,
        reload=reload,
        port=port,
        host=host,
        log_level=log_level,
    )


@toolkit.command()
@click.option("--force", is_flag=True, default=False, type=bool)
@click.option("--purge", is_flag=True, default=False, type=bool)
@coro
async def initial_setup(force: bool, purge: bool):
    from app.models import TranslationUnits
    from json import load

    with open("default-units.json", "r") as file:
        units = load(file)

    await connect()

    if purge:
        _units = await TranslationUnits.query.gino.all()
        for unit in _units:
            await unit.delete()

    langs = units.keys()
    for lang in langs:
        for unit, items in units[lang].items():
            trans = await TranslationUnits.get_unit(lang=lang, unit=unit)
            if trans is not None and force:
                await trans.update(
                    unit=unit, default=items["default"], label=items["label"]
                ).apply()

            else:
                await TranslationUnits.create(
                    lang=lang, unit=unit, default=items["default"], label=items["label"]
                )


@toolkit.command()
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Are you sure you want to drop the db?",
)
@coro
async def dropdb():
    """Drop Database"""
    from app import db

    await connect()
    await db.gino.drop_all()
    click.echo("Database dropped")


@toolkit.command()
@click.option("--name", prompt="New Name")
@click.option("--email", prompt="New E-Mail")
@click.password_option()
@click.option("--issuperuser", is_flag=True, prompt="Is Superuser")
@coro
async def adduser(name, email, password, issuperuser):
    """Add user to database"""
    from app.models import User

    await connect()
    await User.create(
        username=name,
        password=User.gen_password(password),
        e_mail=email,
        is_superuser=issuperuser,
    )
    return


if __name__ == "__main__":
    toolkit()
