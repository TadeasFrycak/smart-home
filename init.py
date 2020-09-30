from library.clients import Clients
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

from flask_login import LoginManager, UserMixin
from flask import Flask
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_babel_js import BabelJS
import datetime
import socket
import os


try:
    from library.raspberry import Raspberry

except ModuleNotFoundError as e:
    pass

# Define constants and variables
OK = "ok"
INDEX = "index"

users = []
slide_index_change = [0, 0]

# Initialise
database = SQLAlchemy()

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="")
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
    role = database.Column(database.String(20), nullable=False, default="visitor")
    username = database.Column(database.String(81), nullable=False, unique=True)
    password = database.Column(database.String(100), nullable=False)
    register_date = database.Column(database.DateTime, nullable=False, default=datetime.datetime.utcnow)
    mode = database.Column(database.String(5), nullable=False, default="smart")

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
werkzeug_logger = WerkzeugLogger(priority=int(fmng.config["logs"]["werkzeug_priority"]))
auth_logger = AuthLogger(priority=int(fmng.config["logs"]["auth_priority"]))
console_logger = ConsoleLogger(priority=int(fmng.config["logs"]["console_priority"]))
console = Console(logger=console_logger, priority=int(fmng.config["logs"]["console_priority"]), socket_io=socketio)
default_values = DefaultValues(fmng=fmng)
refactoring = Refactoring()
tmng_r = TemplateManagerRead(fmng=fmng, console=console, default_values=default_values, refactoring=refactoring)
tmng_rwr = TemplateManagerRewrite(fmng=fmng, tmng_r=tmng_r, default_values=default_values)
tmng_w = TemplateManagerWrite(fmng=fmng, tmng_r=tmng_r, tmng_rwr=tmng_rwr)
html_json = HTML_JSON()
auth = Auth(fmng=fmng, logger=auth_logger)
validator = Validator(fmng=fmng, tmng_r=tmng_r, refactoring=refactoring, console=console)
imng = ImageManager(fmng=fmng, console=console)
sun = Sun(latitude=float(fmng.config["position"]["latitude"]), longitude=float(fmng.config["position"]["longitude"]))
prevent_hack = PreventHack()
app.jinja_env.globals.update(refactor=refactoring.refactor, get_latest_apk=fmng.get_latest_apk)


# Validate files
validate = validator.validate_jsons()
if validate is not True:
    console.print("Error in JSON due: {0}".format(validate), 2)
    exit()

# Check duplicities
check_duplicity = validator.check_duplicity_ids()
if check_duplicity is not True:
    console.print("Duplicity detected in: {0}".format(check_duplicity), 1)

user_id = os.geteuid()
if user_id != 0:  # Is not run as root
    console.print("Run me please with root permission!", 2)
    exit()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    server_ip = s.getsockname()[0]
    s.close()

    print(console.FG_COLORS["white"] + console.SPECIAL["bold"] + "URL:\t" + console.END + "http://" + server_ip + "/")

except OSError as e:
    server_ip = "127.0.0.1"
    print(console.FG_COLORS["white"] + console.SPECIAL["bold"] + "URL:\t" + console.END + "http://127.0.0.1/")

clients = Clients(server_ip=server_ip)
acom = Acom(console=console, socket_io=socketio, ip=server_ip, tmng_rwr=tmng_rwr)

print(console.FG_COLORS["white"] + console.SPECIAL["bold"] + "Mode:\t" + console.END + socketio.async_mode)
print()

try:
    raspberry = Raspberry()

except NameError as e:
    console.print("This device is not a Raspberry!", 1)
    print()

os.environ["WERKZEUG_RUN_MAIN"] = "true"  # Turn off first Werkzeug log to console
