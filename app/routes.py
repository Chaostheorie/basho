from . import app
from .models import Room
from quart import request, render_template


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/rooms/")
@app.route("/rooms/<int:page>")
async def rooms_overview(page: int = 1):
    per_page = request.args.get("per-page", 10)
    rooms = await Room.overview_paginated(offset=(page - 1) * per_page, limit=per_page)
    return await render_template("rooms/overview.html", rooms=rooms)
