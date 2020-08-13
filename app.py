from library.logger import WerkzeugLogger, AuthLogger, ConsoleLogger
from library.tmng_rewrite import TemplateManagerRewrite
from library.tmng_write import TemplateManagerWrite
from library.tmng_read import TemplateManagerRead
from library.default_values import DefaultValues
from library.prevent_hack import PreventHack
from library.refactoring import Refactoring
from library.html_json import HTML_JSON
from library.validator import Validator
from library.imng import ImageManager
from library.fmng import FileManager
from library.console import Console
from library.acom import Acom
from library.auth import Auth
from library.sun import Sun

from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from flask import Flask, session, request, render_template, abort, Blueprint, redirect, url_for
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room, close_room
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import Babel, gettext, lazy_gettext
from flask_sqlalchemy import SQLAlchemy
from flask_babel_js import BabelJS
from getmac import get_mac_address
from subprocess import Popen

import subprocess
import webbrowser
import functools
import unidecode
import datetime
import socket
import base64
import json
import glob
import time
import sys
import os


try:
    from library.raspberry import Raspberry

except Exception as e:
    pass

# TODO oslovování  - použít skloňování (například v logoutu)
# TODO role - najít example na netu, role přiděluje majitel
# TODO user_name --> username
# TODO když se někdo připojí (refreshne stránku) přehraje to Macháčka - DOOBRÝ DEN TA DE A ŠI
# TODO chytré pozadí - co když nenajde žádný tmavý apod.
# TODO nainstalovat eventlet
# TODO detekován podvod - někdo smazal JavaScript (ověřování validity - že není jméno, příjmení prázdné, username pro
#  kontrolu apod) v aplikaci a aplikace poslala nevalidní data ==> zabanovat IP, zabanovat MAC, zabanovat případný
#  další účet (to jméno, pokud se objeví na jiné MAC/IP tak ihned banovat)
# TODO jmenný seznam s daty svátku --> připomenout, kdy má kdo svátek
# TODO zakázat registrace
# TODO notifikace při registrování/loginu jsou nevhodné, musí se to udělat jinak
# TODO hodně pokusů o přihlášení --> blokovat, např často/hodně pokusů
# TODO místo logging použít logguru (rychlejší, když jsou logy staré, smaže je) - mazat logy pokud jsou staré
#  (dohodnout se ještě)
# TODO více nastavení v configu
# TODO user musí obsahovat i background - výchozí random (smart)
# TODO kontrolovat po JavaScriptu některé kontroly, jako například login, register, ale taky move_slide_index
#  (co když je na konci a chce posunout doprava), ...
# TODO validace JavaScriptu, CSS, HTML

# Define constants and variables
OK = "ok"
INDEX = "index"

users = []

# Initialise
database = SQLAlchemy()

app = Flask(__name__, static_url_path="")
app.config.from_object("data.server_config.flask.DevelopmentConfig")

socketio = SocketIO(app=app, cookie=app.config["SOCKETIO_COOKIE_NAME"], async_mode=None)
babel = Babel(app=app)
babeljs = BabelJS(app=app)

database.init_app(app=app)

lmng = LoginManager()
lmng.init_app(app=app)


class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    first_name = database.Column(database.String(40), nullable=False)
    last_name = database.Column(database.String(40), nullable=False)
    permission = database.Column(database.String(20), default="visitor")
    username = database.Column(database.String(81), unique=True)
    password = database.Column(database.String(100), nullable=False)
    register_date = database.Column(database.DateTime, nullable=False, default=datetime.datetime.utcnow)
    sex = database.Column(database.String(6))
    mode = database.Column(database.String(5), default="smart")

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {0}>".format(self.username)


database.create_all(app=app)

# Initialise own modules
fmng = FileManager()
werkzeug_logger = WerkzeugLogger(priority=fmng.config["logs"]["werkzeug_priority"])
auth_logger = AuthLogger(priority=fmng.config["logs"]["auth_priority"])
console_logger = ConsoleLogger(priority=fmng.config["logs"]["console_priority"])
console = Console(logger=console_logger, priority=fmng.config["logs"]["console_priority"], socket_io=socketio)
default_values = DefaultValues()
refactoring = Refactoring()
tmng_r = TemplateManagerRead(fmng=fmng, console=console, default_values=default_values, refactoring=refactoring)
tmng_rwr = TemplateManagerRewrite(fmng=fmng, tmng_r=tmng_r, default_values=default_values)
tmng_w = TemplateManagerWrite(fmng=fmng, tmng_r=tmng_r, tmng_rwr=tmng_rwr)
html_json = HTML_JSON()
auth = Auth(fmng=fmng, logger=auth_logger)
validator = Validator(fmng=fmng, tmng_r=tmng_r)
imng = ImageManager(fmng=fmng, console=console)
sun = Sun(latitude=fmng.config["position"]["latitude"], longitude=fmng.config["position"]["longitude"])
prevent_hack = PreventHack()

app.jinja_env.globals.update(refactor=refactoring.refactor)


try:
    raspberry = Raspberry()

except Exception as e:
    console.print("This device is not a Raspberry! Some functions may not work correctly!", 1)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    server_ip = s.getsockname()[0]
    acom = Acom(console=console, socket_io=socketio, ip=server_ip, tmng_rwr=tmng_rwr)
    s.close()

    print(console.FG_COLORS["blue"] + console.SPECIAL["bold"] + "Server IP address: " + console.END + server_ip + ":5000")

except Exception as e:
    server_ip = "127.0.0.1"
    print(console.FG_COLORS["blue"] + console.SPECIAL["bold"] + "Server IP address: " + console.END + "127.0.0.1:5000")

print(console.FG_COLORS["blue"] + console.SPECIAL["bold"] + "Current mode: " + console.END + socketio.async_mode)

# Validate files
validate = validator.validate_jsons()
if validate is not True:
    console.print("Error in JSON due: {0}".format(validate), 2)
    exit()

# Check duplicities
check_duplicity = validator.check_duplicity_ids()
if check_duplicity is not True:
    console.print("Duplicity detected in: {0}".format(check_duplicity), 1)


def socketio_login_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@lmng.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@lmng.unauthorized_handler
def unauthorized_handler():
    print(datetime.datetime.utcnow())
    ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

    if server_ip == ip:
        mac = get_mac_address(hostname="localhost")
    else:
        mac = get_mac_address(ip=ip)

    mac_list = fmng.mac_list
    mode = sun.day_or_night_now()

    if mac not in mac_list:
        mac_list.append(mac)
        fmng.mac_list = mac_list

        # TODO
        return render_template("auth/register.html", background_image=imng.random_background(bg_type=mode),
                               mode=mode, introduction=fmng.config["introduction"], redirect=request.url_rule)

    else:
        return render_template("auth/login.html", background_image=imng.random_background(bg_type=mode), mode=mode,
                               redirect=request.url_rule)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])


# Add meta header
@app.after_request
def add_meta(response):
    """
    Add meta to HTMLs - it doesn't cache in Chrome, Safari, ...
    :param response: header
    :return: response
    """

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


# Error pages
@app.errorhandler(401)
def access_denied(event):
    return render_template("error.html", header=401, message=str(event))


@app.errorhandler(403)
def access_denied(event):
    return render_template("error.html", header=403, message=str(event))


@app.errorhandler(404)
def page_not_found(event):
    return render_template("error.html", header=404, message=str(event))


@app.errorhandler(410)
def gone(event):
    return render_template("error.html", header=410, message=str(event))


@app.errorhandler(500)
def internal_server_error(event):
    return render_template("error.html", header=500, message=str(event))


# @app.errorhandler(Exception)
# def page_not_found(event):
#    return render_template("error.html", header="Other", message=str(event))


@app.route("/esp/<data>", methods=["GET", "POST"])
def esp(data):
    socketio.emit("notify", {"title": "Kostka", "message": "Nová pozice: " + data, "type": "warning"}, namespace=app.config["SOCKETIO_NAMESPACE"], broadcast=True)
    return OK


@app.route("/login", methods=["POST"])
def login():
    for user in users:
        print(login_user(user["user"], user["remember"]))

    return OK

# TODO http://quabr.com:8182/60186473/is-there-a-way-to-login-a-user-using-flask-socket-io


# @app.route("/pass")
# def login_pass():
#     login_user( User.query.filter_by(username="tadeas.frycak").first(), True)
#     return "OK"


@socketio.on("user_change_mode", namespace=app.config["SOCKETIO_NAMESPACE"])
def user_change_mode(data):
    mode = data["mode"]

    user = User.query.filter_by(username=current_user.username).first()
    user.mode = mode
    database.session.commit()

    emit("user_change_mode_result", {"mode": sun.get_mode(user_mode=mode)}, room=current_user.username)


@socketio.on("login", namespace=app.config["SOCKETIO_NAMESPACE"])
def login_socketio(data):
    ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

    if server_ip == ip:
        mac = get_mac_address(hostname="localhost")
    else:
        mac = get_mac_address(ip=ip)

    username = data["username"].strip()
    password = data["password"]
    remember = data["remember"]

    user = User.query.filter_by(username=username).first()
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user.check_password(password):
        auth_logger.warning(
            "Wrong login! User '{0}' from IP '{1}' with MAC '{2}' and header '{3}'".format(username, ip, mac,
                                                                                           request.user_agent))
        emit("login_result", {"status": False})

    else:
        auth_logger.debug("Login on user '{0}' on IP '{1}' with MAC '{2}' and header '{3}'".format(username, ip, mac,
                                                                                                   request.user_agent))
        users.append({"user": user, "remember": remember})

        # TODO
        # print(login_user(user, remember=remember))

        emit("login_result", {"status": True})


@app.route("/logout")
@login_required
def logout():
    user = {"first_name": current_user.first_name, "last_name": current_user.last_name,
            "username": current_user.username, "sex": current_user.sex}

    mode = sun.get_mode(current_user.mode)

    logout_user()
    return render_template("auth/logout.html", user=user, background_image=imng.random_background(bg_type=mode), mode=mode)


@app.route("/register")
def register():
    if current_user.is_authenticated:
        abort(404)

    else:
        mode = sun.day_or_night_now()
        return render_template("auth/register.html", background_image=imng.random_background(bg_type=mode), mode=mode, redirect="/")


@socketio.on("register", namespace=app.config["SOCKETIO_NAMESPACE"])
def register_socketio(data):
    first_name = data["first_name"].strip().capitalize()
    last_name = data["last_name"].strip().capitalize()
    username = data["username"].strip()
    password = data["password"]
    password_repeat = data["password_repeat"]
    sex = data["sex"].strip()

    # TODO ochrany jako username != heslo apodobně
    #print(prevent_hack.check(first_name=first_name, last_name=last_name, username=username, password=password,
    #                         password_repeat=password_repeat, sex=sex))
    user = User.query.filter_by(username=username).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        emit("register_result", {"status": False})

    else:
        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(first_name=first_name, last_name=last_name, username=username, sex=sex)
        new_user.set_password(password)

        # add the new user to the database
        database.session.add(new_user)
        database.session.commit()

        emit("register_result", {"status": True})


# Index page
@app.route("/")
@login_required
def index():
    mode = sun.get_mode(user_mode=current_user.mode)
    return render_template("index.html", slides=fmng.devices, background_image=imng.random_background(bg_type=mode), mode=mode)


@app.route("/edit")
@login_required
def edit():
    mode = sun.get_mode(user_mode=current_user.mode)
    return render_template("index.html", slides=fmng.devices, background_image=imng.random_background(bg_type=mode), mode=mode, edit=True)


@app.route("/devices")
@login_required
def devices_return():
    return str(fmng.devices)


@socketio.on("save", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def save_devices():
    fmng.devices = fmng.devices


# Tile
@socketio.on("tile_value", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def tile_value(data):
    tile_id = data[tmng_r.ID]
    value = int(data[tmng_r.VALUE])

    console.print("Change tile (ID: {0}) value to {1}".format(tile_id, str(value)))

    emit("tile_value_result", {tmng_r.ID: tile_id, tmng_r.VALUE: value}, broadcast=True)
    acom.mqtt_thread.publish(tile_id=tile_id, value=value)
    tmng_rwr.tile_value(new_value=value, tile_id=tile_id)


@socketio.on("tile_id", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def tile_id_rwr(data):
    tile_id = data["tile_id"]
    new_id = data["new_id"]

    console.print("Change tile ID from {0} to {1}".format(tile_id, str(new_id)))
    tmng_rwr.tile_id(tile_id=tile_id, new_id=new_id)

    emit("tile_id_result", {"tile_id": tile_id, "new_id": new_id}, broadcast=True)


@socketio.on("tile_index", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def tile_index(data):
    old_index = int(data["old_index"])
    new_index = int(data["new_index"])
    slide_index = int(data["slide_index"])

    console.print("Change tile index from {0} to {1} on slide {2}".format(str(old_index), str(new_index),
                                                                          str(slide_index)))

    tmng_rwr.tile_index(old_index=old_index, new_index=new_index, slide_index=slide_index)
    emit("tile_index_result", {"old_index": old_index, "new_index": new_index, "slide_index": slide_index},
         broadcast=True, include_self=False)


@socketio.on("tile_label", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def tile_label(data):
    """
    Rewrite tile name
    :return:
    """

    tile_id = data[tmng_r.TILE_ID]
    new_label = data["new_label"]

    console.print("Change tile (ID: {0}) label to {1}".format(tile_id, str(new_label)))
    tmng_rwr.tile_label(tile_id=tile_id, new_label=new_label)

    emit("tile_label_result", {"tile_id": tile_id, "new_label": new_label}, broadcast=True)


@socketio.on("tile_dynamic_value", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def tile_dynamic_value(data):
    tile_id = data[tmng_r.TILE_ID]
    new_value = data["new_value"]
    value_name = refactoring.refactor_reverse(data["value_name"])

    console.print("Change tile (ID: {0}) dynamic value {1} to {2}".format(tile_id, value_name, new_value))
    tmng_rwr.tile_dynamic_value(tile_id=tile_id, new_value=new_value, value_name=value_name)
    # TODO refresh celého HTML
    # refresh(tile_id=tile_id)


@socketio.on("tile_type", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def tile_type(data):
    tile_id = data[tmng_r.TILE_ID]
    old_type = tmng_r.get_tile_type(tile_id=tile_id)
    new_type = refactoring.refactor_reverse(data["new_type"])

    if old_type != new_type:
        console.print("Change tile (ID: {0}) type to {1}".format(tile_id, new_type))

        tile = tmng_r.get_tile(tile_id)
        old_tile_values = render_template(fmng.path_join("modal_edit", "tile_values.html"), tile_values=tmng_r.get_tile_template_values(tile_type=old_type, tile_id=tile_id))
        new_tile_values = render_template(fmng.path_join("modal_edit", "tile_values.html"), tile_values=tmng_r.get_tile_template_values(tile_type=new_type, tile_id=tile_id))

        if old_tile_values == new_tile_values:
            tile_values = None

        else:
            tile_values = new_tile_values

        tmng_rwr.tile_type(new_type=new_type, tile_id=tile_id)

        emit("tile_type_result", {"tile_values": tile_values, "tile_id": tile_id, "tile_html": render_template(fmng.path_join("tiles", tmng_r.get_tile_type(tile_id) + ".html"), tile=tile)}, broadcast=True)


@socketio.on("tile_icon", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def tile_icon(data):
    tile_id = data[tmng_r.TILE_ID]
    new_icon = data["new_icon"]

    if tmng_rwr.tile_icon(new_icon=new_icon, tile_id=tile_id):
        console.print("Change tile (ID: {0}) icon to {1}".format(tile_id, new_icon))

        emit("tile_icon_result", {"tile_id": tile_id, "new_icon": "/img/icons/" + new_icon}, broadcast=True)


@socketio.on("tile_delete", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def tile_delete(data):
    tile_id = data[tmng_r.TILE_ID]

    console.print("Delete tile (ID: {0})".format(tile_id))
    tmng_w.tile_delete(tile_id=tile_id)

    emit("tile_delete_result", {"tile_id": tile_id}, broadcast=True)


# Modal
@socketio.on("get_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def get_modal(data):
    tile_id = data[tmng_r.TILE_ID]
    tile = tmng_r.get_tile(tile_id)

    console.print("Opening modal for {0}...".format(tile_id))
    emit("get_modal_result", {"modal": render_template("modal.html", tile=tile),
                              "graphs": tmng_r.get_modal_graphs(tile_id=tile_id),
                              "daterangepickers": tmng_r.get_modal_daterangepickers(tile_id=tile_id),
                              "tile_id": tile_id})


@socketio.on("get_edit_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def get_edit_modal(data):
    tile_id = data[tmng_r.TILE_ID]
    tile_type = tmng_r.get_tile_type(tile_id)

    console.print("Opening edit modal for {0} - tile type is {1}...".format(tile_id, tile_type))
    emit("get_edit_modal_result",
         {"modal": render_template("modal_edit.html", modal=tmng_r.get_tile(tile_id)[tmng_r.MODAL],
                                   modal_items=tmng_r.get_modal_templates(),
                                   tile_values=tmng_r.get_tile_template_values(tile_type=tile_type, tile_id=tile_id),
                                   tile_types=tmng_r.get_tile_templates(), tile_type=tile_type, tile_id=tile_id)})


@socketio.on("get_add_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def get_add_modal(data):
    slide_index = int(data["slide_index"])

    tile_type = default_values.TILE_TYPE
    new_tile = default_values.tile()
    tile_html = render_template(fmng.path_join("tiles", tile_type + ".html"), tile=new_tile)
    fmng.devices[slide_index]["children"].append(new_tile)

    console.print("Opening add modal")

    emit("get_add_tile_result", {"tile_html": tile_html, "slide_index": slide_index}, broadcast=True)
    emit("get_add_modal_result", {"modal": render_template("modal_edit.html",
                                                           modal_items=tmng_r.get_modal_templates(),
                                                           tile_values=tmng_r.get_tile_template_values(tile_type=tile_type),
                                                           tile_types=tmng_r.get_tile_templates(),
                                                           tile_type=tile_type, tile_id=new_tile["data"]["id"])})


@socketio.on("get_settings_modal", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def get_modal_settings():
    backgrounds = fmng.list_file_names(path=imng.IMG_PATH)
    console.print("Opening settings modal...")
    # TODO nefunguje
    emit("get_settings_modal_result", {"modal": render_template("modal_settings.html", modal=fmng.settings,
                                                                backgrounds=backgrounds)})


@socketio.on("add_modal_item", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def add_modal_item(data):
    item_type = refactoring.refactor_reverse(data[tmng_r.TYPE])
    tile_id = data[tmng_r.TILE_ID]

    console.print("Append modal item {0} to tile {1}".format(item_type, tile_id))

    emit("add_modal_item_result", {"item": render_template("modal_edit/item_values.html", tile_id=tile_id,
                                                           item=tmng_w.append_modal_item(item_type=item_type,
                                                                                         tile_id=tile_id)),
                                   "tile_id": tile_id}, broadcast=True)


# Modal events
@socketio.on("modal_slider", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def modal_slider(data):
    item_id = data[tmng_r.ID]
    new_value = data[tmng_r.VALUE]
    tile_id = data[tmng_r.TILE_ID]

    tmng_rwr.modal_slider(tile_id=tile_id, item_id=item_id, new_value=new_value)
    emit("modal_slider_result", {"id": item_id, "tile_id": tile_id, "value": new_value}, broadcast=True, include_self=False)

    acom.mqtt_thread.publish(tile_id=tile_id, item_id=item_id, value=new_value)


@socketio.on("modal_toggle", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def modal_toggle(data):
    item_id = data[tmng_r.ID]
    new_value = int(data[tmng_r.VALUE])
    tile_id = data[tmng_r.TILE_ID]

    console.print("New value of modal toggle (ID: {0}) in tile {1} is {2}".format(item_id, tile_id, str(new_value)))

    acom.mqtt_thread.publish(tile_id=tile_id, item_id=item_id, value=new_value)
    print(tmng_rwr.modal_toggle(tile_id=tile_id, item_id=item_id, new_value=new_value))
    emit("modal_toggle_result", {"id": item_id, "tile_id": tile_id, "value": new_value}, broadcast=True, include_self=False)

    # TODO If current tile is Raspberry tile - Make for Raspberry static tile
    if tile_id == "raspberry-1":
        if item_id == "raspberry-birds":
            subprocess.check_output(["omxplayer", "birds.mp3"]).decode("utf-8")

        elif item_id == "raspberry-halt":
            emit("notify", {"title": "Kontaktuji...", "message": "Kontaktuji všechna zařízení...",
                            "type": "info"}, broadcast=True)
            time.sleep(3)
            emit("notify", {"title": "Vypínání...", "message": "Nebude již možné kontrolovat zařízení",
                            "type": "danger"}, broadcast=True)
            subprocess.check_output(["sudo", "halt"]).decode("utf-8")


@socketio.on("modal_daterangepicker", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def daterangepicker(data):
    item_id = data[tmng_r.ID]
    start_value = data["start_value"]
    end_value = data["end_value"]
    pair_id = data["pair_id"]
    tile_id = data[tmng_r.TILE_ID]

    console.print("New value of modal daterangepicker (ID: {0}) in tile {1} is: start value {2} and end value {3}".format(item_id, tile_id, start_value, end_value))
    tmng_rwr.modal_daterangepicker(tile_id=tile_id, item_id=item_id, start_value=start_value, end_value=end_value)

    emit("graph_rwr", {"graph_id": pair_id, "value": tmng_r.get_modal_graphs(tile_id=tile_id, item_id=pair_id)}, broadcast=True)


# Modal rewrite
@socketio.on("modal_item_index", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def modal_item_index(data):
    tile_id = data[tmng_r.ID]
    old_index = int(data["old_index"])
    new_index = int(data["new_index"])

    emit("modal_item_index_result", {"tile_id": tile_id, "old_index": old_index, "new_index": new_index}, broadcast=True, include_self=False)
    console.print("Change modal item index in tile (ID: {0}) from {1} to {2}".format(tile_id, old_index, new_index))
    tmng_rwr.modal_item_index(new_index=new_index, old_index=old_index, tile_id=tile_id)


@socketio.on("modal_item_dynamic_value", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def modal_item_value(data):
    tile_id = data[tmng_r.TILE_ID]
    value_name = refactoring.refactor_reverse(data["value_name"])
    new_value = data["new_value"]
    item_index = int(data[INDEX])

    console.print("Change modal item value ({0}) in tile (ID: {1}) to {2} (item index is {3})".format(value_name, tile_id, new_value, str(item_index)))
    tmng_rwr.modal_item_value(new_value=new_value, value_name=value_name, tile_id=tile_id, index=item_index)


@socketio.on("modal_item_delete", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def modal_item_delete(data):
    tile_id = data[tmng_r.TILE_ID]
    item_index = int(data[INDEX])

    emit("modal_item_delete_result", {"tile_id": tile_id, "index": item_index}, broadcast=True)

    console.print("Delete modal item in tile (ID: {0}) from index {1}".format(tile_id, str(item_index)))
    tmng_w.modal_item_delete(index=item_index, tile_id=tile_id)


# Swiper
@socketio.on("slide_name", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def slide_name(data):
    slide_index = int(data[INDEX])
    new_name = data["new_name"]

    console.print("Change slide (index: {0}) name to {1}".format(str(slide_index), new_name))
    tmng_rwr.slide_name(index=slide_index, new_name=new_name)


@socketio.on("slide_append", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def slide_append():
    tmng_w.append_slide()
    console.print("Append new slide")

    emit("slide_append_result", {"slide": render_template("slide.html", slide={"name": "Bez názvu"})}, broadcast=True)
    emit("slide_append_animation_result")


@socketio.on("slide_prepend", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def slide_prepend():
    tmng_w.prepend_slide()
    console.print("Prepend new slide")

    emit("slide_prepend_result", {"slide": render_template("slide.html", slide={"name": "Bez názvu"})}, broadcast=True)
    emit("slide_prepend_animation_result")


@socketio.on("slide_index", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def slide_prepend(data):
    old_index = data["old_index"]
    new_index = data["new_index"]

    tmng_rwr.slide_index(old_index=old_index, new_index=new_index)
    console.print("Changing slide index from {0} to {1}".format(str(old_index), str(new_index)))
    emit("slide_index_result", {"new_index": new_index, "old_index": old_index}, broadcast=True)


@socketio.on("slide_delete", namespace=app.config["SOCKETIO_NAMESPACE"])
@socketio_login_required
def slide_delete(data):
    slide_index = data[INDEX]

    console.print("Delete slide (index: {0})".format(slide_index))
    tmng_w.delete_slide(index=slide_index)

    emit("slide_delete_animation_result")
    emit("slide_delete_result", {"index": slide_index}, broadcast=True)  # TODO když bude na slajdě, udělat taky animaci


# Client connect/disconnect
@socketio.on("connect", namespace=app.config["SOCKETIO_NAMESPACE"])
def client_connect():
    """
    Event on user connect
    :return:
    """

    if current_user.is_authenticated:
        join_room(current_user.username)

    console.print("Client {0} ({4}) connected with {2} v{3} ({1})".format(request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                                                                          str(request.accept_languages),
                                                                          str(request.user_agent.browser),
                                                                          str(request.user_agent.version),
                                                                          str(request.sid)))


@socketio.on("disconnect", namespace=app.config["SOCKETIO_NAMESPACE"])
def client_disconnect():
    """
    Event on user disconnect
    :return:
    """

    if current_user.is_authenticated:
        leave_room(current_user.username)

    console.print("Client {0} ({4}) disconnected with {2} v{3} ({1})".format(request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                                                                             str(request.accept_languages),
                                                                             str(request.user_agent.browser),
                                                                             str(request.user_agent.version),
                                                                             str(request.sid)))


# TODO loginrequiered
# Server operations
@app.route("/shutdown", methods=["POST", "GET"])
def shutdown():
    """
    Shutdown server
    :return: confirmation of server shutdown
    """

    print(console.FG_COLORS["green"] + console.SPECIAL["bold"] + "I must clean space after me! Wait pls" + console.END)  # TODO
    # TODO (vyčistit logy, pycache, ...) - na to udělat .sh soubor
    print(console.FG_COLORS["fail"] + console.SPECIAL["bold"] + "Server shutdown" + console.END)
    werkzeug_shutdown = request.environ.get("werkzeug.server.shutdown")

    if werkzeug_shutdown is None:
        console.print("Not running with the Werkzeug Server", 2)

    werkzeug_shutdown()  # Shutdown server

    return render_template("error.html", header="Vypnuto", message="Server byl úspěšně vypnut")


# TODO loginrequiered
@app.route("/restart", methods=["POST", "GET"])
def restart():
    """
    Restart server
    :return: confirmation of server restart - display only if it is GET request
    """

    print(console.FG_COLORS["fail"] + console.SPECIAL["bold"] + "Server is restarting..." + console.END)

    Popen([sys.executable, "app.py"])  # Open new app.py
    werkzeug_shutdown = request.environ.get("werkzeug.server.shutdown")

    if werkzeug_shutdown is None:
        console.print("Not running with the Werkzeug Server", 2)

    werkzeug_shutdown()  # Shutdown current server
    return render_template("error.html", header="Restart", message="Server byl úspěšně restartován")


@app.route("/reload", methods=["POST", "GET"])
@login_required
def reload():
    """
    Reload page in all opened browsers
    :return: confirmation of browsers reload - display only if it is GET request
    """

    print(console.FG_COLORS["fail"] + console.SPECIAL["bold"] + "Server is reloading all active browsers..." + console.END)
    socketio.emit("reload", {}, namespace=app.config["SOCKETIO_NAMESPACE"], broadcast=True)  # Send acom request to reload page on all browsers
    return render_template("error.html", header="Reload",
                           message="Všechny webové prohlížeče práve obnovili svoje stránky s Chytrou domácností")  # TODO překlad


os.environ["WERKZEUG_RUN_MAIN"] = "true"  # Turn off first Werkzeug log to console

# Run whole application
if __name__ == "__main__" and bool(fmng.config["run"]) is True:
    # TODO only on start not restart
    # webbrowser.open(server_ip + ":5000")
    socketio.run(app=app, host=str(fmng.config["host"]))

else:
    console.print("Stopped - see server_config", 2)
