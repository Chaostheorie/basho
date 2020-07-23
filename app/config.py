__doc__ = """
File containing initial configuration and startup/ shutdown coroutines
"""

import os
from os import getenv
from quart import Config as BaseConfig
from dotenv import load_dotenv
from .helper import gen_secret, coro
from atexit import register

# Load Env variables
load_dotenv()


def get_url() -> str:
    if os.environ.get("CI"):
        # See github workflow files
        return f"postgres://postgres:postgres@127.0.0.1"
    if (url := getenv("DATABASE_URL")) is not None:
        return url
    url = f"{getenv('DRIVER')}://{getenv('DATABASE-USER')}:{getenv('PASSWORD')}@{getenv('ADDRESS')}/{getenv('DATABASE')}"
    if url.find("None") != -1:
        raise EnvironmentError("Environment Variable for Database url was not found")
        print(url)
    return url


class config:
    DATABASE_URL = get_url()
    HTTPSREDIRECT = getenv("HTTPSREDIRECT", 0)
    DEBUG = getenv("DEBUG", True)


async def LoadDB() -> None:
    """Loads the DB classes to prevent metadata overwriting"""
    from . import app
    from .models import User

    # All Table models need to be loaded to be attached to db.metadata
    app.logger.info("Database initialised")


def bind_on_shutdown() -> None:
    register(coro(disconnect()))


async def disconnect() -> None:
    """Disconnects from database"""
    from . import app

    await app.engine.pop_bind().close()
    app.logger.info("Database connection closed")
