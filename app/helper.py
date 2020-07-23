import typing
from quart import Quart, request
from os import getenv
from asyncio import run


async def connect():
    """Connect to database, establishes and creates tables"""
    from . import db, app
    from .config import LoadDB

    await LoadDB()
    await db.set_bind(app.config.get("DATABASE_URL"))


def gen_secret() -> bytes:
    from os import urandom

    print(
        "\033[93mWARNING\033[0m: Secret was not specified and random secret will be used"
    )
    return urandom(64)


def coro(f):
    return run(f)


class TranslationCache:
    def __init__(
        self, app: Quart, langs: typing.List[str] = ["en", "de"], refresh: bool = True
    ):
        self.translations, self.app, self.langs = dict.fromkeys(langs), app, langs
        self.default = app.config.get("BABEL_DEFAULT_LOCALE", "en")

    def get_unit(self, lang: str, unit: str) -> typing.Dict[str, str]:
        print(self.translations["en"])
        if lang in self.langs:
            unit = self.translations[lang].get(unit, None)
        else:
            return self.translations[self.default].get(unit, None)

    async def refresh(self):
        """Refreshes translation unit cache from database"""
        from .models import TranslationUnits

        for lang in self.langs:
            units = await TranslationUnits.query.where(
                TranslationUnits.lang == lang
            ).gino.all()
            for unit in units:
                if self.translations[lang] is None:
                    self.translations[lang] = {}
                if unit.translation is None:
                    self.translations[lang][unit.unit] = unit.default
                else:
                    self.translations[lang][unit.unit] = unit.translation
