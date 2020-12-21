from gevent import monkey; monkey.patch_all()  # thread=True, select=False)

from config.items.general import Items
from library.doorbird import Doorbird
from library.logger import AuthLogger, TerminalLogger, ChangesLogger, ChangesEditLogger
from library.tmng_rewrite import TemplateManagerRewrite
from library.tmng_write import TemplateManagerWrite
from library.tmng_read import TemplateManagerRead
from library.default_values import DefaultValues
from library.prevent_hack import PreventHack
from library.clients import Clients, Refresh
from library.refactoring import Refactoring
from library.validator import Validator
from library.imng import ImageManager
from library.fmng import FileManager
from library.terminal import Terminal
from library.acom import Acom
from library.auth import Auth
from library.sun import Sun

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_babel_js import BabelJS
from flask_babel import Babel
from flask import Flask
# import eventlet
import platform
import datetime
import urllib3
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

users = []

# Initialise
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# eventlet.monkey_patch()

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="")
app.config.from_object("config.flask.DevelopmentConfig")
app.config["TRAP_HTTP_EXCEPTIONS"] = True

database = SQLAlchemy(app=app)
socketio = SocketIO(app=app, cookie=app.config["SOCKETIO_COOKIE_NAME"], async_mode=None)  # , message_queue="redis://")
babel = Babel(app=app)
babeljs = BabelJS(app=app)
lmng = LoginManager(app=app)


class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    first_name = database.Column(database.String(20), nullable=False)
    last_name = database.Column(database.String(20), nullable=False)
    role = database.Column(database.String(20), nullable=False, default="visitor")
    username = database.Column(database.String(40), nullable=False, unique=True)
    password = database.Column(database.String(80), nullable=False)
    register_date = database.Column(database.DateTime, nullable=False, default=datetime.datetime.utcnow)
    mode = database.Column(database.String(5), nullable=False, default="smart")
    background = database.Column(database.String(5), nullable=False, default="smart")

    # Todo https://docs-sqlalchemy.readthedocs.io/ko/latest/core/type_basics.html
    # TODO několik dalších věcí jako login_dates, mac_adress, ips, ...

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def set_sex(self, sex):
        # gender.Detector(case_sensitive=False)
        # self.sex = TODO prozatím sem mrksni hádač (gender)
        pass

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {0}>".format(self.username)


database.create_all(app=app)

# Initialise own modules
fmng = FileManager()

auth_logger = AuthLogger(priority=int(fmng.config["logs"]["auth_priority"]))
terminal_logger = TerminalLogger(priority=int(fmng.config["logs"]["terminal_priority"]))
changes_logger = ChangesLogger(priority=int(fmng.config["logs"]["changes_priority"]))
changes_edit_logger = ChangesEditLogger(priority=int(fmng.config["logs"]["changes_edit_priority"]))

terminal = Terminal(logger=terminal_logger, priority=int(fmng.config["logs"]["terminal_priority"]), socket_io=socketio)
default_values = DefaultValues(fmng=fmng)
refactoring = Refactoring()
default_items = Items()
tmng_r = TemplateManagerRead(fmng=fmng, terminal=terminal, default_values=default_values, refactoring=refactoring, default_items=default_items)
tmng_rwr = TemplateManagerRewrite(fmng=fmng, tmng_r=tmng_r, default_values=default_values, default_items=default_items)
tmng_w = TemplateManagerWrite(fmng=fmng, tmng_r=tmng_r, tmng_rwr=tmng_rwr, default_values=default_values)
auth = Auth(fmng=fmng, logger=auth_logger)
validator = Validator(fmng=fmng, tmng_r=tmng_r, refactoring=refactoring, terminal=terminal)
sun = Sun(latitude=float(fmng.config["position"]["latitude"]), longitude=float(fmng.config["position"]["longitude"]))
prevent_hack = PreventHack()
doorbird = Doorbird(ip=fmng.config["doorbird"]["ip"], username=fmng.config["doorbird"]["username"], password=fmng.config["doorbird"]["password"])
app.jinja_env.globals.update(refactor=refactoring.refactor,
                             refactor_remove=refactoring.refactor_remove,
                             get_time_ago=refactoring.get_time_ago,
                             get_latest_apk=fmng.get_latest_apk)
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

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    server_ip = s.getsockname()[0]
    s.close()

except OSError as e:
    server_ip = "127.0.0.1"

clients = Clients(server_ip=server_ip)
refresh_clients = Refresh(fmng=fmng)
acom = Acom(terminal=terminal, socket_io=socketio, ip=server_ip, tmng_r=tmng_r, tmng_rwr=tmng_rwr, refactoring=refactoring, app=app, doorbird=doorbird, sun=sun, refresh_clients=refresh_clients)

# TODO terminal indent auto
# terminal.print(terminal.FG_COLORS["white"] + terminal.SPECIAL["bold"] + "\t\t\t\t\tIn dev:\t" + terminal.END + refactoring.get_time_ago(time.mktime(datetime.datetime.strptime("26.05.2019 17:29", "%d.%m.%Y %H:%M").timetuple())))
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

# if socketio.async_mode != "eventlet":
#     terminal.error("Run me please with 'eventlet' instead of '{}'!".format(socketio.async_mode))
#     exit()

try:
    raspberry = Raspberry()

except NameError as e:
    terminal.warning("This device is not a Raspberry!")

imng = ImageManager(fmng=fmng, terminal=terminal)

os.environ["WERKZEUG_RUN_MAIN"] = "true"  # Turn off first Werkzeug log to terminal
