# This is the code for the Flask web server
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

import camera
import config

# init camera capture for every camera listed in config


app = Flask(__name__)
app.secret_key = config.get("secret_key")

login_manager = LoginManager(app)

# need to make a user class to make flask_login happy
class User(UserMixin):
    def __init__(self, id, password_hash):
        self.id = id
        self.password_hash = password_hash

ADMIN_USER = User(0, config.get('password_hash'))

def conditional_login_required(condition: bool):
    '''A wrapper for the login_required decorator that can be turned on or off based on a condition'''
    def decorator_wrapper(func):
        if not condition:
            return login_required(func)
        return func
    return decorator_wrapper

@login_manager.user_loader
def load_user(user_id):
    return ADMIN_USER

@app.errorhandler(401)
def unauthorized(e):
    return render_template("login.html")

@app.route("/")
@conditional_login_required(config.get("view_perm"))
def index():
    camera_data = config.get("camera_data")
    return render_template("index.html", camera_data=camera_data)

@app.route("/feed")
@conditional_login_required(config.get("view_perm"))
def feed():
    device_name = request.args.get("device_name")
    return render_template("feed.html", image_data=camera.get_image_b64(device_name), device_name=device_name)

@app.route("/get_image_b64")
@conditional_login_required(config.get("view_perm"))
def get_image_b64():
    device_name = request.args.get("device_name")
    return camera.get_image_b64(device_name)

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    password = request.form.get('password')
    remember = request.form.get('remember')

    if not check_password_hash(ADMIN_USER.password_hash, password):
        flash("Please check your login details and try again.")
        return redirect(url_for('login'))

    login_user(ADMIN_USER, remember=remember)
    return redirect(url_for("settings"))

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

@app.route("/logout")
def logout():
    logout_user()
    return render_template("logout.html")

if __name__ == "__main__":
    app.run("0.0.0.0")