# -*- coding=utf-8 -*-
#!/usr/bin/env python3

__version__ = "v0.0.1b0"
__author__ = "Cobalt"
__license__ = "MIT @ Cobalt"

import quart.flask_patch
from quart import Quart
from flask_babel import Babel
from asyncio import run
from quart_auth import AuthManager
from .gino_quart import Gino
from .config import config
from logging import getLogger

app = Quart(__name__)

# Set metadata
app.version = __version__
app.license = __license__

app.config.from_object(config)
app.log = getLogger("Boardgame-Backend")
app.babel = Babel(app)
db = Gino(app=app, dsn=app.config.get("DATABASE_URL"))
app.auth = AuthManager(app)
app.secret_key = app.config.get("SECRET")

# Load models
from .models import *

# Import routes
from .routes import *

# Import auth stuff
from .auth import *

# import filters
from .filters import *

# Load translation unit cache
from .helper import TranslationCache

app.translations = TranslationCache(app)

# before serving
@app.before_serving
async def refresh():
    await app.translations.refresh()
