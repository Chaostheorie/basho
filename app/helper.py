from os import getenv
from asyncio import run


async def connect():
    """Connect to database, establishes and creates tables"""
    from . import db, app
    from .config import LoadDB

    await LoadDB()
    await db.set_bind(app.config.DATABASE_URL)


def gen_secret() -> bytes:
    from os import urandom

    print(
        "\033[93mWARNING\033[0m: Secret was not specified and random secret will be used"
    )
    return urandom(64)


def coro(f):
    return run(f)
