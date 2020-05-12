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
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_babel import Babel, _, gettext, ngettext, lazy_gettext
from flask_babel_js import BabelJS
from subprocess import Popen
from getmac import get_mac_address

import subprocess
import webbrowser
import unidecode
import datetime
import socket
import json
import glob
import time
import sys
import os


try:
    from library.raspberry import Raspberry

except Exception as e:
    pass

# TODO doplnit všechny překlady
# TODO nainstalovat eventlet
# TODO podle pingu určovat zda je connection slow nebo fast
# TODO slow internet - slow connection - images in low quality, ultra slow internet - dont send images
# TODO detekován podvod - někdo smazal JavaScript (ověřování validity - že není jméno, příjmení prázdné, username pro
#  kontrolu apod) v aplikaci a aplikace poslala nevalidní data
# TODO rozdělit app.py na několik soborů pomocí Blueprint
# TODO pokud detekuje podvodníka, zabanovat IP, zabanovat MAC, zabanovat případný další účet
#  (to jméno, pokud se objeví na jiné MAC/IP tak ihned banovat)
# TODO zkontrolovat, zda se jedná o jméno --> jmenný seznam s daty svátku --> připomenout, kdy má kdo svátek -->
#  připoměnout majiteli svátek
# TODO bezpečnost - javascript dostane heslo, ... apodobně, aby nemohl uživatel udělat svůj vlastní JS jednoduše
# TODO zakázat registrace
# TODO notifikace při registrování/loginu jsou nevhodné, musí se to udělat jinak
# TODO user musí obsahovat array of user MACs and IPs, all login date
# TODO hodně pokusů o přihlášení --> blokovat, např často/hodně pokusů
# TODO místo logging použít logguru (rychlejší, když jsou logy staré, smaže je) - mazat logy pokud jsou staré
#  (dohodnout se ještě)

# Define constants
OK = "ok"
INDEX = "index"

# Initialise Flask
database = SQLAlchemy()

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
app.config.from_object("data.server_config.flask.DevelopmentConfig")

socketio = SocketIO(app=app, cookie=app.config["SOCKETIO_COOKIE_NAME"], async_mode=None)
babel = Babel(app=app)
babeljs = BabelJS(app=app)

database.init_app(app=app)
database.create_all(app=app)

lmng = LoginManager()
lmng.login_view = "login"
lmng.init_app(app)

print("Current mode:" + socketio.async_mode)


class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    first_name = database.Column(database.String(40))
    last_name = database.Column(database.String(40))
    permission = database.Column(database.String(20))
    user_name = database.Column(database.String(81), unique=True)
    password = database.Column(database.String(100))
    register_date = database.Column(database.String(40))
    sex = database.Column(database.String(6))
    mode = database.Column(database.String(5))


# Initialise own modules
fmng = FileManager()
werkzeug_logger = WerkzeugLogger(priority=fmng.config["werkzeug_priority"])
auth_logger = AuthLogger(priority=fmng.config["auth_priority"])
console_logger = ConsoleLogger(priority=fmng.config["console_priority"])
console = Console(logger=console_logger, priority=fmng.config["console_priority"], socket_io=socketio)
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
    console.print("This device is not a Raspberry! Some\nfunctions may not work correctly!", 1)

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

# Validate files
validate = validator.validate_jsons()
if validate is not True:
    console.print("Error in JSON due: {0}".format(validate), 2)
    exit()

# Check duplicities
check_duplicity = validator.check_duplicity_ids()
if check_duplicity is not True:
    console.print("Duplicity detected in: {0}".format(check_duplicity), 1)


def refresh(tile_id=None, remove=False):
    tile_content = tmng_r.get_tile(tile_id=tile_id)
    slide_index = tmng_r.get_slide_index(tile_id=tile_id)

    if not remove:
        socketio.emit("tile_refresh",
                      {"tile": render_template(fmng.path_join("tiles", tmng_r.get_tile_type(tile_id) + ".html"),
                                                tile=tile_content), tmng_r.ID: tile_id, "slide_index": slide_index,
                        "tile_id": tile_id}, namespace="/acom")
    else:
        socketio.emit("tile_refresh",
                      {"tile": "", tmng_r.ID: tile_id, "slide_index": slide_index,
                        "tile_id": tile_id}, namespace="/acom")


@lmng.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


# TODO udělat, že se po přihlášení bude muset jednou za čas uživatel přihlásit
# login_manager.refresh_view = "accounts.reauthenticate"
# login_manager.needs_refresh_message = (
#    u"To protect your account, please reauthenticate to access this page."
# )
# login_manager.needs_refresh_message_category = "info"
# @login_manager.needs_refresh_handler
# def refresh():
#     # do stuff
#     return a_response

@lmng.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login", next=request.url))


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


@app.route("/logout")
@login_required
def logout():
    user = {"first_name": current_user.first_name, "last_name": current_user.last_name,
            "user_name": current_user.user_name, "sex": current_user.sex}

    mode = current_user.mode
    if mode == "smart":
        new_mode = sun.day_or_night_now()

    else:
        new_mode = mode

    logout_user()
    return render_template("auth/logout.html", user=user, background_image=imng.random_background(bg_type=new_mode), mode=mode)


@app.route("/esp/<data>", methods=["GET", "POST"])
def esp(data):
    socketio.emit("notify", {"title": "Kostka", "message": "Nová pozice: " + data,
                              "type": "warning"}, namespace="/acom")
    return OK


@app.route("/login", methods=["GET", "POST"])
def login():
    ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

    if server_ip == ip:
        mac = get_mac_address(hostname="localhost")
    else:
        mac = get_mac_address(ip=ip)

    mac_list = fmng.mac_list
    if mac not in mac_list:
        mac_list.append(mac)
        fmng.mac_list = mac_list

        mode = sun.day_or_night_now()

        return render_template("auth/register.html", background_image=imng.random_background(bg_type=mode),
                               mode=mode, introduction=True)

    if request.method == "POST":
        user_name = request.form.get("user_name", None)
        password = request.form.get("password", None)
        remember = bool(int(request.form.get("remember", False)))

        user = User.query.filter_by(user_name=user_name).first()

        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.password, password):
            auth_logger.warning("Wrong login! User '{0}' from IP '{1}' with MAC '{2}' and header '{3}'".format(user_name, ip, mac, request.user_agent))
            socketio.emit("notify", {"title": "Špatné heslo", "message": "Omlouvám se, ale tohle heslo je špatné!",
                           "type": "danger"}, namespace="/acom")
            return redirect(url_for("login"))  # if user doesn't exist or password is wrong, reload the page

        auth_logger.debug("Login on user '{0}' on IP '{1}' with MAC '{2}' and header '{3}'".format(user_name, ip, mac, request.user_agent))
        login_user(user, remember=remember)

        next_page = request.form.get("next")
        if next_page == "%2F":
            return url_for("index")

        else:
            return next_page or url_for("index")

    else:
        mode = sun.day_or_night_now()
        return render_template("auth/login.html", background_image=imng.random_background(bg_type=mode), mode=mode)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name", None).strip()
        last_name = request.form.get("last_name", None).strip()
        user_name = request.form.get("user_name", None).strip()
        permission = request.form.get("permission", None)
        password = request.form.get("password", None)
        password_repeat = request.form.get("password_repeat", None)
        register_date = request.form.get("register_date", None)
        sex = request.form.get("sex", None)
        mode = request.form.get("mode", None)

        print(prevent_hack.check(first_name=first_name, last_name=last_name, user_name=user_name, password=password,
                                 password_repeat=password_repeat, register_date=register_date, sex=sex, mode=mode,
                                 permission=permission))
        user = User.query.filter_by(user_name=user_name).first()  # if this returns a user, then the email already exists in database

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            socketio.emit("notify", {"title": "Účet již existuje", "message": "Omlouvám se, ale tenhle účet již existuje!",
                                      "type": "danger"}, namespace="/acom")
            # TODO ochrany jako username != heslo apodobně
            print("no tak to teda v žádným případě")
            return redirect(url_for('register'))

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(first_name=first_name, last_name=last_name, user_name=user_name, permission=permission, sex=sex,
                        register_date=register_date, mode=mode,
                        password=generate_password_hash(password, method="sha256"))

        # add the new user to the database
        database.session.add(new_user)
        database.session.commit()
        return url_for("index")
    else:
        mode = sun.day_or_night_now()
        return render_template("auth/register.html", background_image=imng.random_background(bg_type=mode),
                               mode=mode)


# Index page
@app.route("/")
@login_required
def index():
    """
    Render index page
    :return: index page
    """

    mode = current_user.mode
    if mode == "smart":
        new_mode = sun.day_or_night_now()

    else:
        new_mode = mode

    return render_template("index.html", slides=fmng.devices, user={"first_name": current_user.first_name,
                                                                    "last_name": current_user.last_name,
                                                                    "user_name": current_user.user_name,
                                                                    "sex": current_user.sex},
                           background_image=imng.random_background(bg_type=new_mode), mode=new_mode)


@app.route("/edit")
@login_required
def edit():
    mode = current_user.mode

    if mode == "smart":
        new_mode = sun.day_or_night_now()

    else:
        new_mode = mode

    return render_template("index.html", slides=fmng.devices, background_image=imng.random_background(bg_type=new_mode),
                           mode=new_mode, edit=True)


@app.route("/devices")
@login_required
def devices_return():
    return str(fmng.devices)


@app.route("/save", methods=["GET", "POST"])
@login_required
def save_devices():
    fmng.devices = fmng.devices
    return str(fmng.devices)


def graph_rwr(tile_id, data_x, data_y):
    # Get pages (number and content)
    for page_num, page_content in enumerate(fmng.devices):
        # Get tiles (number and content)
        for item_num, item_content in enumerate(page_content[tmng_r.DATA]):
            # If that tile is current opened tile, rewrite
            if item_content[tmng_r.DATA][tmng_r.ID] == tile_id:
                for num, i in enumerate(item_content[tmng_r.MODAL]):
                    if i["type"] == "graph":
                        fmng.devices[page_num][tmng_r.DATA][item_num][tmng_r.MODAL][num]["data"]["data_x"].append(data_x)
                        fmng.devices[page_num][tmng_r.DATA][item_num][tmng_r.MODAL][num]["data"]["data_y"].append(data_y)
                return True


@app.route("/sklenik/<data>")
def greenhouse(data):
    split = data.split(";")
    socketio.emit("notify", {"title": "Skleník", "message": "{0} °C; {1} %".format(split[0], split[1]),
                              "type": "success"}, namespace="/acom")
    split = data.split(";")

    tmng_rwr.tile_value(tile_id="greenhouse-temp", new_value=float(split[0]))
    tmng_rwr.tile_value(tile_id="greenhouse-hum", new_value=float(split[1]))
    refresh("greenhouse-temp")
    refresh("greenhouse-hum")
    time_x = str(datetime.datetime.now())
    graph_rwr(tile_id="greenhouse-temp", data_x=time_x, data_y=float(split[0]))
    graph_rwr(tile_id="greenhouse-hum", data_x=time_x, data_y=float(split[1]))

    return OK


# Tile
@app.route("/tile", methods=["POST"])
@login_required
def tile():
    """
    Tile click event
    :return:
    """

    tile_id = request.form[tmng_r.ID]  # TODO přepsat na request.form.get("cochci", vychozi_hodnota)
    value = int(request.form[tmng_r.VALUE])

    console.print("Change tile (ID: {0}) value to {1}".format(tile_id, str(value)))
    socketio.emit("tile", {tmng_r.ID: tile_id, tmng_r.VALUE: value}, namespace="/acom")

    acom.mqtt_thread.publish(tile_id=tile_id, value=value)
    tmng_rwr.tile_value(new_value=value, tile_id=tile_id)

    return OK


@app.route("/get_tile", methods=["POST"])
@login_required
def get_tile():
    """
    Get HTML of tile by ID
    :return: HTML of tile
    """

    tile_id = request.form["tile_id"]
    tile_content = tmng_r.get_tile(tile_id=tile_id)

    if tile_content is not None:
        return json.dumps({"tile": render_template(fmng.path_join("tiles", tmng_r.get_tile_type(tile_id) + ".html"),
                                                   tile=tile_content), tmng_r.ID: tile_id, "tile_id": tile_id})

    else:
        return "None"


@app.route("/tile_id_rwr", methods=["POST"])
@login_required
def tile_id_rwr():
    """
    Rewrite tile ID
    :return:
    """

    tile_id = request.form["tile_id"]
    new_id = request.form["new_id"]

    console.print("Change tile ID from {0} to {1}".format(tile_id, str(new_id)))
    tmng_rwr.tile_id(tile_id=tile_id, new_id=new_id)

    return OK


@app.route("/tile_index_rwr", methods=["POST"])
@login_required
def tile_index_rwr():
    """
    Rewrite tile ID
    :return:
    """

    old_index = int(request.form["old_index"])
    new_index = int(request.form["new_index"])
    slide = int(request.form["slide"])

    console.print("Change tile index from {0} to {1} on slide {2}".format(str(old_index), str(new_index), str(slide)))

    tmng_rwr.tile_index(old_index=old_index, new_index=new_index, slide=slide)

    return OK


@app.route("/tile_name_rwr", methods=["POST"])
@login_required
def tile_name_rwr():
    """
    Rewrite tile name
    :return:
    """

    tile_id = request.form["tile_id"]
    new_name = request.form["new_name"]

    console.print("Change tile (ID: {0}) name to {1}".format(tile_id, str(new_name)))
    tmng_rwr.tile_name(tile_id=tile_id, new_name=new_name)
    refresh(tile_id=tile_id)

    return OK


@app.route("/tile_dynamic_value_rwr", methods=["POST"])
@login_required
def tile_value_rwr():
    tile_id = request.form["tile_id"]
    new_value = request.form["new_value"]
    value_name = refactoring.refactor_reverse(request.form["value_name"])

    console.print("Change tile (ID: {0}) dynamic value {1} to {2}".format(tile_id, value_name, new_value))
    tmng_rwr.tile_dynamic_value(tile_id=tile_id, new_value=new_value, value_name=value_name)
    refresh(tile_id=tile_id)

    return OK


@app.route("/tile_type_rwr", methods=["POST"])
@login_required
def tile_type_rwr():
    """
    Rewrite tile type
    :return:
    """

    tile_id = request.form[tmng_r.ID]
    new_type = refactoring.refactor_reverse(request.form["new_type"])

    console.print("Change tile (ID: {0}) type to {1}".format(tile_id, new_type))
    tmng_rwr.tile_type(new_type=new_type, tile_id=tile_id)
    refresh(tile_id=tile_id)

    return json.dumps({"tile_values": render_template(fmng.path_join("modal_edit", "tile_values.html"),
                                                      tile_values=tmng_r.get_tile_template_values(tile_type=new_type,
                                                                                                  tile_id=tile_id))})


@app.route("/tile_icon_rwr", methods=["POST"])
@login_required
def tile_icon_rwr():
    """
    Rewrite tile type
    :return:
    """

    tile_id = request.form[tmng_r.ID]
    new_icon = request.form["new_icon"]

    if tmng_rwr.tile_icon(new_icon=new_icon, tile_id=tile_id):
        console.print("Change tile (ID: {0}) icon to {1}".format(tile_id, new_icon))
        refresh(tile_id=tile_id)

    return OK


@app.route("/tile_delete", methods=["POST"])
@login_required
def tile_delete():
    """
    Rewrite tile typet(
    :return:
    """

    tile_id = request.form[tmng_r.ID]
    refresh(tile_id=tile_id, remove=True)

    console.print("Delete tile (ID: {0})".format(tile_id))
    tmng_w.tile_delete(tile_id=tile_id)

    return OK


# Modal
@app.route("/get_modal", methods=["POST"])
@login_required
def get_modal():
    tile_id = request.form[tmng_r.ID]

    # emit("notify", {"title": "Message", "message": "Halooo2",
    #                "type": "warning"})

    console.print("Opening modal for {0}...".format(tile_id))
    return json.dumps({"modal": render_template("modal.html", modal=tmng_r.get_tile(tile_id)[tmng_r.MODAL]),
                       "graphs": tmng_r.get_modal_graphs(tile_id=tile_id),
                       "daterangepickers": tmng_r.get_modal_daterangepickers(tile_id=tile_id)})


@app.route("/get_edit_modal", methods=["POST"])
@login_required
def get_edit_modal():
    tile_id = request.form[tmng_r.ID]

    tile_type = tmng_r.get_tile_type(tile_id)
    console.print("Opening edit modal for {0} - tile type is {1}...".format(tile_id, tile_type))
    return json.dumps({"modal": render_template("modal_edit.html",  # TODO dát pryč modal
                                                modal=tmng_r.get_tile(tile_id)[tmng_r.MODAL],
                                                modal_items=tmng_r.get_modal_templates(),
                                                tile_values=tmng_r.get_tile_template_values(tile_type=tile_type,
                                                                                            tile_id=tile_id),
                                                tile_types=tmng_r.get_tile_templates(),
                                                tile_type=tile_type,
                                                tile_id=tile_id)})


@app.route("/get_add_tile_modal", methods=["POST"])
@login_required
def get_add_tile_modal():
    slide_index = int(request.form["slide_index"])

    tile_type = default_values.TILE_TYPE
    new_tile = default_values.tile()
    fmng.devices[slide_index]["children"].append(new_tile)

    refresh(new_tile["data"]["id"])
    console.print("Opening add modal")

    return json.dumps({"modal": render_template("modal_edit.html",
                                                modal_items=tmng_r.get_modal_templates(),
                                                tile_values=tmng_r.get_tile_template_values(tile_type=tile_type),
                                                tile_types=tmng_r.get_tile_templates(),
                                                tile_type=tile_type,
                                                tile_id=new_tile["data"]["id"])})


@app.route("/add_modal_edit_item", methods=["POST"])
@login_required
def add_modal_edit_item():
    """
    Add new item (like slider or toggle) into modal in edit mode
    :return: HTML of item
    """

    item_type = refactoring.refactor_reverse(request.form[tmng_r.TYPE])
    tile_id = request.form[tmng_r.TILE_ID]

    console.print("Append modal item {0} to tile {1}".format(item_type, tile_id))

    return json.dumps({"item": render_template("modal_edit/item_values.html", tile_id=tile_id,
                                               item=tmng_w.append_modal_item(item_type=item_type, tile_id=tile_id))})


@app.route("/get_modal_settings", methods=["POST"])
@login_required
def get_modal_settings():
    backgrounds = fmng.list_file_names(path=imng.IMG_PATH)
    console.print("Opening settings modal...")
    return json.dumps({"modal": render_template("modal_settings.html", modal=fmng.settings, backgrounds=backgrounds)})


# Modal events
@app.route("/slider", methods=["POST"])
@login_required
def slider():
    """
    Slider item event
    :return:
    """

    json_data = request.form.to_dict(flat=True)
    item_id = request.form[tmng_r.ID]
    new_value = request.form[tmng_r.VALUE]
    tile_id = request.form[tmng_r.TILE_ID]

    tmng_rwr.modal_slider(tile_id=tile_id, item_id=item_id, new_value=new_value)
    socketio.emit("slider", json_data, namespace="/acom")

    acom.mqtt_thread.publish(tile_id=tile_id, item_id=item_id, value=new_value)

    return OK


@app.route("/toggle", methods=["POST"])
@login_required
def toggle():
    """
    Toggle item event
    :return:
    """

    json_data = request.form.to_dict(flat=True)

    item_id = request.form[tmng_r.ID]
    new_value = int(request.form[tmng_r.VALUE])
    tile_id = request.form[tmng_r.TILE_ID]

    console.print("New value of modal toggle (ID: {0}) in tile {1} is {2}".format(item_id, tile_id, str(new_value)))

    acom.mqtt_thread.publish(tile_id=tile_id, item_id=item_id, value=new_value)
    socketio.emit("toggle", json_data, namespace="/acom")

    # TODO If current tile is Raspberry tile - Make for Raspberry static tile
    if tile_id == "raspberry-1":
        if item_id == "raspberry-birds":
            subprocess.check_output(["omxplayer", "birds.mp3"]).decode("utf-8")

        elif item_id == "raspberry-halt":
            fmng.write_file(fmng.path_join(fmng.SERVER_CONFIG_DIR, fmng.DEVICES_FILE), fmng.devices, True)
            socketio.emit("notify", {"title": "Kontaktuji...", "message": "Kontaktuji všechna zařízení...",
                                      "type": "info"}, namespace="/acom")
            time.sleep(3)
            socketio.emit("notify", {"title": "Vypínání...", "message": "Nebude již možné kontrolovat zařízení",
                                      "type": "danger"}, namespace="/acom")
            subprocess.check_output(["sudo", "halt"]).decode("utf-8")

        return OK

    tmng_rwr.modal_toggle(tile_id=tile_id, item_id=item_id, new_value=new_value)

    return OK

@app.route("/datarangepicker", methods=["POST"])
@login_required
def datarangepicker():
    """
    Toggle item event
    :return:
    """

    item_id = request.form[tmng_r.ID]
    start_value = request.form["start_value"]
    end_value = request.form["end_value"]
    pair_id = request.form["pair_id"]
    tile_id = request.form[tmng_r.TILE_ID]

    console.print("New value of modal daterangepicker (ID: {0}) in tile {1} is: start value {2} and end value {3}".format(item_id, tile_id, start_value, end_value))
    tmng_rwr.modal_daterangepicker(tile_id=tile_id, item_id=item_id, start_value=start_value, end_value=end_value)

    socketio.emit("graph_rwr", {"graph_id": pair_id, "value": tmng_r.get_modal_graphs(tile_id=tile_id, item_id=pair_id)}, namespace="/acom")

    return OK


# Modal rewrite
@app.route("/modal_item_index_rwr", methods=["POST"])
@login_required
def modal_item_index_rwr():
    """
    Change order of items in modal (from old_index to new_index)
    :return:
    """

    tile_id = request.form[tmng_r.ID]
    old_index = int(request.form["old_index"])
    new_index = int(request.form["new_index"])

    console.print("Change modal item index in tile (ID: {0}) from {1} to {2}".format(tile_id, old_index, new_index))
    tmng_rwr.modal_item_index(new_index=new_index, old_index=old_index, tile_id=tile_id)

    return OK


@app.route("/modal_item_value_rwr", methods=["POST"])
@login_required
def modal_item_value_rwr():
    """
    Rewrite any value of item
    :return:
    """

    tile_id = request.form[tmng_r.TILE_ID]
    value_name = refactoring.refactor_reverse(request.form["value_name"])
    new_value = request.form["new_value"]
    item_index = int(request.form[INDEX])

    console.print("Change modal item value ({0}) in tile (ID: {1}) to {2} (item index is {3})".format(value_name, tile_id, new_value, str(item_index)))

    tmng_rwr.modal_item_value(new_value=new_value, value_name=value_name, tile_id=tile_id, index=item_index)

    return OK


@app.route("/modal_item_delete", methods=["POST"])
@login_required
def modal_item_delete():
    """
    Delete modal item
    :return:
    """

    tile_id = request.form[tmng_r.TILE_ID]
    item_index = int(request.form[INDEX])

    console.print("Delete modal item in tile (ID: {0}) from index {1}".format(tile_id, str(item_index)))
    tmng_w.modal_item_delete(index=item_index, tile_id=tile_id)

    return OK


# Swiper
@app.route("/slide_name", methods=["POST"])
@login_required
def slide_name():
    """
    Change page name
    :return:
    """

    slide_index = int(request.form[INDEX])
    new_name = request.form["new_name"]

    console.print("Change slide (index: {0}) name to {1}".format(str(slide_index), new_name))
    tmng_rwr.slide_name(index=slide_index, new_name=new_name)

    return OK


@app.route("/append_slide", methods=["POST"])
@login_required
def append_slide():
    """
    Append new slide
    :return:
    """

    tmng_w.append_slide()
    console.print("Append new slide")
    return json.dumps({"slide": render_template("slide.html", slide={"name": "Bez názvu"})})


@app.route("/delete_slide", methods=["POST"])
@login_required
def delete_slide():
    """
    Remove current slide (by index)
    :return:
    """

    page_index = int(request.form[INDEX])

    console.print("Delete slide (index: {0})".format(page_index))
    tmng_w.delete_slide(index=page_index)

    return OK


clients = []


# Client connect/disconnect
@socketio.on("connect", namespace="/acom")
def client_connect():
    """
    Event on user connect
    :return:
    """
    clients.append(request.sid)
    print(clients)
    console.print("Client {0} connected with {2} v{3} ({1})".format(request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                                                                    str(request.accept_languages),
                                                                    str(request.user_agent.browser),
                                                                    str(request.user_agent.version)))


@socketio.on("disconnect", namespace="/acom")
def client_disconnect():
    """
    Event on user disconnect
    :return:
    """
    clients.remove(request.sid)
    print(clients)
    console.print("Client {0} disconnected with {2} v{3} ({1})".format(request.environ.get("HTTP_X_REAL_IP", request.remote_addr),
                                                                       str(request.accept_languages),
                                                                       str(request.user_agent.browser),
                                                                       str(request.user_agent.version)))


# TODO loginrequiered
# Server operations
@app.route("/shutdown", methods=["POST", "GET"])
def shutdown():
    """
    Shutdown server
    :return: confirmation of server shutdown
    """

    print(console.FG_COLORS["green"] + console.SPECIAL["bold"] + "I must clean space after me! Wait pls" + console.END)  # TODO
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


@socketio.on('my_event', namespace="/acom")
def handle_my_custom_event(asdf):
    print(asdf)
    print(type(asdf))


@app.route("/reload", methods=["POST", "GET"])
@login_required
def reload():
    """
    Reload page in all opened browsers
    :return: confirmation of browsers reload - display only if it is GET request
    """

    print(console.FG_COLORS["fail"] + console.SPECIAL["bold"] + "Server is reloading all active browsers..." + console.END)
    socketio.emit("reload", {}, namespace="/acom")  # Send acom request to reload page on all browsers
    return render_template("error.html", header="Reload",
                           message="Všechny webové prohlížeče práve obnovili svoje stránky s Chytrou domácností")


os.environ["WERKZEUG_RUN_MAIN"] = "true"  # Turn off first Werkzeug log to console

# Run whole application
if __name__ == "__main__" and bool(fmng.config["run"]) is True:
    # TODO only on start not restart
    # webbrowser.open(server_ip + ":5000")
    socketio.run(app=app, host=str(fmng.config["host"]))
    # app.run(host=str(fmng.config["host"]))

else:
    console.print("Stopped - see server_config", 2)
