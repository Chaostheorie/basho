from . import app
from .models import Room, User, TranslationUnits
from .schemas import UserRegisterSchema
from flask_babel import get_locale
from quart import request, render_template, Response, abort, redirect


@app.route("/")
async def index():
    return await render_template("index.html")


# Rooms
@app.route("/rooms/")
@app.route("/rooms/<int:page>")
async def rooms_overview(page: int = 1):
    per_page = request.args.get("per-page", 10)
    rooms = await Room.overview_paginated(offset=(page - 1) * per_page, limit=per_page)
    return await render_template("rooms/overview.html", rooms=rooms)


# Admin
@app.route("/admin/units/edit/<unit>", methods=["GET", "POST"])
async def edit_unit(unit: str) -> Response:
    if request.method == "GET":
        units = await TranslationUnits.get_units(unit=unit)
        if units == []:
            abort(404)
        return await render_template("admin/unit-edit.html", units=units)
    else:
        vals = await request.values
        print(vals)
        print(vals["en[unit]"])
        return "", 200

# Users
@app.route("/users")
async def user_overview() -> Response:
    """Route for user overview. Contains table with user and search

    Returns:
        Response: [description]
    """
    users = await User.query.gino.all()
    return await render_template("admin/users.html", users=users)


@app.route("/users/edit/<int:id>", methods=["GET", "POST"])
async def edit_user_route(id: int) -> Response:
    """Route for user editing. Gives either template response or processes and redirects

    Args:
        id (int): [description]
    """
    if request.method == "GET":
        return await render_template("admin/edit.html")
    else:
        print(request.values())
        if UserDataSchema(request.values):
            print("Update User data")
        else:
            return abort(401)

@app.before_request
async def evaluate_locale():
    request.locale = get_locale()
