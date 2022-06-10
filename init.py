import random
import string

import gevent.monkey; gevent.monkey.patch_all()  # patch_thread() # thread=True, select=False)
from library.logger import AuthLogger, TerminalLogger, ChangesLogger, ChangesEditLogger
from library.tmng_rewrite import TemplateManagerRewrite
from library.tmng_write import TemplateManagerWrite
from library.tmng_read import TemplateManagerRead
from config.protocols.general import Protocols
from library.prevent_hack import PreventHack
from library.clients import Clients, Refresh
from library.refactoring import Refactoring
from library.updater import Updater
from library.validator import Validator
from config.items.general import Items
from config.tiles.general import Tiles
from library.imng import ImageManager
from library.terminal import Terminal
from library.fmng import FileManager
from library.acom import Acom
from library.auth import Auth
from library.sun import Sun

from flask_socketio import join_room, leave_room
from flask_login import login_user, logout_user, login_required
from flask import redirect
from flask_socketio import emit, disconnect
from flask import request, render_template, abort
from flask_login import current_user
from flask_babel import gettext
import functools
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_babel_js import BabelJS
from flask_babel import Babel
from flask import Flask
import platform
import datetime
import inspect
import htmlmin
# import eventlet
import socket
import sys
import os


try:
    from library.raspberry import Raspberry

except ModuleNotFoundError as e:
    pass

# Define constants and variables
OK = "ok"
INDEX = "index"

# Initialise
# eventlet.monkey_patch()
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__, static_url_path="/static")
app.config.from_object("config.flask.DevelopmentConfig")
app.config["TRAP_HTTP_EXCEPTIONS"] = True

database = SQLAlchemy(app=app)
socketio = SocketIO(app=app, cookie=app.config["SOCKETIO_COOKIE_NAME"], async_mode=None)
babel = Babel(app=app)
babeljs = BabelJS(app=app)
lmng = LoginManager(app=app)


class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    first_name = database.Column(database.String(20), nullable=False)
    last_name = database.Column(database.String(20), nullable=False)
    role = database.Column(database.String(20), nullable=False, default="visitor")
    username = database.Column(database.String(40), nullable=False, unique=True)
    salt = database.Column(database.String(8), nullable=False)
    password = database.Column(database.String(80), nullable=False)
    register_date = database.Column(database.DateTime, nullable=False, default=datetime.datetime.utcnow)
    mode = database.Column(database.String(5), nullable=False, default="smart")
    background = database.Column(database.String(5), nullable=False, default="smart")

    # Todo https://docs-sqlalchemy.readthedocs.io/ko/latest/core/type_basics.html
    # TODO několik dalších věcí jako login_dates, mac_adress, ips, ...

    @staticmethod
    def __generate_salt(n=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

    def set_password(self, password):
        self.salt = self.__generate_salt()
        self.password = generate_password_hash(self.salt + password, method="sha256")

    def set_sex(self, sex):
        # gender.Detector(case_sensitive=False)
        # self.sex = TODO prozatím sem mrksni hádač (gender)
        pass

    def check_password(self, password):
        return check_password_hash(self.password, self.salt + password)

    def __repr__(self):
        return "<User {0}>".format(self.username)


database.create_all(app=app)

# Initialise own modules
fmng = FileManager()

auth_logger = AuthLogger(
    priority=int(fmng.config["logs"]["auth_priority"])
)
terminal_logger = TerminalLogger(
    priority=int(fmng.config["logs"]["terminal_priority"])
)
changes_logger = ChangesLogger(
    priority=int(fmng.config["logs"]["changes_priority"])
)
changes_edit_logger = ChangesEditLogger(
    priority=int(fmng.config["logs"]["changes_edit_priority"])
)

terminal = Terminal(
    logger=terminal_logger,
    priority=int(fmng.config["logs"]["terminal_priority"]),
    socket_io=socketio,
    log_only=fmng.config["logs"].getboolean("log_only")
)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    server_ip = s.getsockname()[0]
    s.close()

except OSError as e:
    server_ip = "127.0.0.1"

if fmng.config["logs"].getboolean("log_only") is False:
    terminal.go_back(10)
    terminal.print(terminal.FG_COLORS["black"] + terminal.BG_COLORS["white"] + terminal.SPECIAL["bold"] + "\t\t\t\t\t ↓ Server info ↓ " + terminal.END)
    terminal.print(terminal.FG_COLORS["white"] + terminal.SPECIAL["bold"] + "\t\t\t\t\tURL\t" + terminal.END + "http://" + server_ip + ":" + str(app.config["PORT"]) + "/")
    terminal.print(terminal.FG_COLORS["white"] + terminal.SPECIAL["bold"] + "\t\t\t\t\tPython\t" + terminal.END + sys.version.split()[0])
    terminal.print(terminal.FG_COLORS["white"] + terminal.SPECIAL["bold"] + "\t\t\t\t\tMode\t" + terminal.END + socketio.async_mode)
    terminal.print(terminal.FG_COLORS["white"] + terminal.SPECIAL["bold"] + "\t\t\t\t\tOS\t" + terminal.END + sys.platform + " " + platform.architecture()[0])
    terminal.print(terminal.FG_COLORS["white"] + terminal.SPECIAL["bold"] + "\t\t\t\t\tOS ver\t" + terminal.END + platform.release())

    terminal.go_forward(4)
    terminal.print(terminal.FG_COLORS["black"] + terminal.BG_COLORS["white"] + terminal.SPECIAL["bold"] + " ↓ Logs and other information ↓ " + terminal.END)
    print()

refactoring = Refactoring()
default_items = Items()
default_tiles = Tiles()

tmng_r = TemplateManagerRead(
    fmng=fmng,
    terminal=terminal,
    refactoring=refactoring,
    default_items=default_items,
    default_tiles=default_tiles
)
tmng_rwr = TemplateManagerRewrite(
    fmng=fmng,
    tmng_r=tmng_r,
    default_items=default_items,
    default_tiles=default_tiles
)
tmng_w = TemplateManagerWrite(
    fmng=fmng,
    tmng_r=tmng_r,
    tmng_rwr=tmng_rwr,
    default_items=default_items
)

updater = Updater(fmng=fmng, tmng_r=tmng_r, tmng_rwr=tmng_rwr, tmng_w=tmng_w, socketio=socketio)  # TODO má to smysl? Nesloučit s tmng_r?

default_protocols = Protocols(terminal, updater, fmng, tmng_r)

auth = Auth(
    fmng=fmng,
    logger=auth_logger
)
validator = Validator(
    fmng=fmng,
    tmng_r=tmng_r,
    refactoring=refactoring,
    terminal=terminal
)
sun = Sun(
    latitude=float(fmng.config["position"]["latitude"]),
    longitude=float(fmng.config["position"]["longitude"]))
prevent_hack = PreventHack()
# TODO remove in 11.9
# doorbird = Doorbird(
#     ip=fmng.config["doorbird"]["ip"],
#     username=fmng.config["doorbird"]["username"],
#     password=fmng.config["doorbird"]["password"]
# )


def get_protocols_config():
    return default_protocols.get_protocol_edit_objects()


def tile_publish(tile_id, value):
    tile = tmng_r.get_tile(tile_id)

    if not tile["protocols"]:
        updater.tile_value(tile_id, value)
        emit("notify", {"title": gettext("Warning"), "message": gettext("This tile is not paired to any protocol!"),
                        "type": "warning", "delay": 5000})

    for protocol in tile["protocols"]:
        default_protocols.get_object(protocol["type"]).publish(config=protocol["config"], value=value)


def item_publish(tile_id, value, item_id):
    item = tmng_r.get_item(tile_id, item_id)

    if not item["protocols"]:
        updater.item_value(tile_id, item_id, value)
        emit("notify", {"title": gettext("Warning"), "message": gettext("This item is not paired to any protocol!"),
                        "type": "warning", "delay": 5000})

    for protocol in item["protocols"]:
        default_protocols.get_object(protocol["type"]).publish(config=protocol["config"], value=value)


app.jinja_env.globals.update(
    refactor=refactoring.refactor,
    refactor_remove=refactoring.refactor_remove,
    get_time_ago=refactoring.get_time_ago,
    get_latest_apk=fmng.get_latest_apk
)
app.jinja_env.add_extension("jinja2.ext.do")

# Validate files
validate = validator.validate_jsons()
if validate is not True:
    terminal.error("Error in JSON due: {0}".format(validate))
    exit()

# Check duplicities
check_duplicity = validator.check_duplicity_ids()
if check_duplicity is not True:
    terminal.warning("Duplicity detected in: {0}".format(check_duplicity))

clients = Clients(server_ip=server_ip)
refresh_clients = Refresh(fmng=fmng)
acom = Acom(
    terminal=terminal,
    socket_io=socketio,
    ip=server_ip,
    tmng_r=tmng_r,
    tmng_rwr=tmng_rwr,
    refactoring=refactoring,
    app=app,
    # doorbird=doorbird,
    sun=sun,
    refresh_clients=refresh_clients,
    fmng=fmng
)

# if socketio.async_mode != "eventlet":
#     terminal.error("Run me please with 'eventlet' instead of '{}'!".format(socketio.async_mode))
#     exit()

imng = ImageManager(fmng=fmng, terminal=terminal)

os.environ["WERKZEUG_RUN_MAIN"] = "true"  # Turn off first Werkzeug log to terminal

# Init protocol listeners
for page_content in fmng.devices:
    # Get tiles (number and content)
    for tile_content in page_content[tmng_r.CHILDREN]:
        tile_id = tile_content["id"]

        for tile_protocol in tile_content["protocols"]:
            default_protocols.get_object(tile_protocol["type"]).add_listener(config=tile_protocol["config"])

        for item_content in tile_content["modal"]:
            for item_protocol in item_content["protocols"]:
                default_protocols.get_object(item_protocol["type"]).add_listener(config=item_protocol["config"])
