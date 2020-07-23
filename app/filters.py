import typing
from . import app
from quart import request
from ujson import dumps
from flask_babel import get_locale
from .models import TranslationUnits


@app.template_filter("get_unit")
def _get_unit_filter(unit):
    return app.translations.get_unit(request.locale, unit)


@app.template_filter("format")
def _format_filter(str, **kwargs):
    return str.format(**kwargs)


@app.template_filter("dictjoin")
def _dict_join_filter(base, *args) -> dict:
    if isinstance(base, list):
        [base[0].update(_base) for _base in base[1:]]
    elif isinstance(base, dict):
        [base.update(_base) for _base in args]
    return base


@app.template_filter("jsonify")
def _jsonify_filter(obj) -> dict:
    if isinstance(obj, list):
        return [_obj.jsonify() for _obj in obj]
    else:
        return obj.jsonify()


@app.template_filter("unitjoin")
def _unit_join_filter(units: typing.List[TranslationUnits]) -> dict:
    res = {}
    for unit in units:
        res[unit.lang] = dict(
            translation=unit.translation,
            default=unit.default,
            id=unit.id,
            unit=unit.unit,
        )
    return res


@app.template_filter("keys")
def _keys_filter(item: dict) -> list:
    return [*item.keys()]
