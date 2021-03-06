import sys
import os
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__))))) # Insert <.>/src

from logging.config import fileConfig
from os import getenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.models import db
from dotenv import load_dotenv
from asyncio import run
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Load Env variables
load_dotenv()

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db
from app.models import *

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    if os.environ.get("CI"):
        # See github workflow files
        return f"postgres://postgres:postgres@127.0.0.1"
    elif (url := getenv("DATABASE_URL")) is not None:
        return url
    url = f"{getenv('DRIVER')}://{getenv('DATABASE-USER')}:{getenv('PASSWORD')}@{getenv('ADDRESS')}/{getenv('DATABASE')}"
    if url.find("None") != -1:
        raise EnvironmentError("Enviroment Variable for Database url was not found")
    return url


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url(),
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
