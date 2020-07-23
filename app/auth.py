from . import app
from quart import redirect, url_for, ResponseReturnValue, request, render_template
from quart_auth import Unauthorized, login_user, logout_user
from .models import User

@app.route("/user/login", methods=["GET", "POST"])
async def login():
    if request.method == "GET":
        return await render_template("auth/login.html")
    else:
        username = request.values.get("username", None)
        password = reqest.values.get("password", None)
        if username is None or password is None:
            abort(401)
        else:
            user = User.get_by_username(username)
            if user.verify_password(password):
                login_user(user)
            else:
                abort(403)

@app.route("/user/logout")
async def logout():
    return redirect("/")

@app.route("/user/profile")
async def user_profile():
    return redirect("/")

@app.route("/user/forgot-password", methods=["GET", "POST"])
async def forgot_password():
    return redirect("/")

@app.errorhandler(Unauthorized)
async def redirect_to_login(*_: Exception) -> ResponseReturnValue:
    return redirect(url_for("login"))
