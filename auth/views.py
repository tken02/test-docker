from flask import request, render_template, url_for, flash, session, jsonify
from flask_login.utils import logout_user
from werkzeug.utils import redirect
from app import app, login_manager
from auth.model import User, LoginForm
from auth.service import getUserById, getUserByUserName
from flask_login import login_user, login_required, AnonymousUserMixin, current_user
import bcrypt
import json


@login_manager.user_loader
def load_user(user_id):
    userDoc = getUserById(user_id)
    if not userDoc:
        return AnonymousUserMixin()

    userObj = json.loads(userDoc.to_json())
    # id field inherited from UserMixin class (from flask_login)
    user = User(
        id=userObj["_id"]["$oid"],
        username=userObj["username"],
        password=userObj["password"],
    )
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"status": "error", "message": "User is not authorized"})


# @csrf.exempt
@app.route("/api/register", methods=["POST"])
def register():
    # pass request data to form
    form = LoginForm()
    # Don't have to pass request.form or check POST request, because
    # validate_on_submit automatically do that
    if form.validate_on_submit():
        data = request.form
        username = data["username"]
        password = data["password"].encode()
        publicKey = data["publick-key"]
        users = getUserByUserName(username)
        if len(users) > 0:
            flash("Username already exists")
            return redirect(url_for("register"))
        salt = bcrypt.gensalt(rounds=16)
        hashPassword = bcrypt.hashpw(password, salt)
        user = User(username=username, password=hashPassword, publicKey=publicKey)
        user.save()
        login_user(user)
        # return redirect(url_for('index'))
        return jsonify(
            {
                "status": "success",
                "data": {"username": username, "public_key": publicKey},
            }
        )

    return jsonify({"status": "error", "message": form.errors})


@app.route("/api/login", methods=["POST"])
def login():
    # pass request data to form
    form = LoginForm()

    # Don't have to pass request.form or check POST request, because
    # validate_on_submit automatically do that
    if form.validate_on_submit():
        data = request.form
        username = data["username"]
        password = data["password"].encode()
        user = getUserByUserName(username).first()
        if not user:
            return redirect(url_for("login"))
        # print(user.to_json())
        if bcrypt.checkpw(password, user.password.encode()):
            login_user(user)
            return jsonify({
                "status": "success",
                "data": {"username": user.username, "public_key": user.publicKey},
            })

    return jsonify({"status": "error", "message": "Invalid login information"})


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    if not current_user.is_anonymous:
        logout_user()
        return jsonify({"status": "success", "data": "User logged out"})

    return jsonify({"status": "error", "message": "User is not logged in"})


# with app.test_client() as c:
# 	rv = c.get('/api/register', data=dict(
# 		username='vinh',
# 		password='asdfasdf',
# 	))
# 	csrf_token = str(rv.data)
# 	rv = c.get('/api/register', data=dict(
# 		username='vinh',
# 		password='asdfasdf',
# 	))
# 	print(rv.data)
# json_data = rv.get_json()
