from library.logger import WerkzeugLogger, AuthLogger, ConsoleLogger
from library.tmng_rewrite import TemplateManagerRewrite
from library.tmng import TemplateManager
from library.html_json import HTML_JSON
from library.validator import Validator
from library.fmng import FileManager
from library.console import Console
from library.arduino import Arduino
from library.auth import Auth

from flask import Flask, request, render_template, abort
from flask_socketio import SocketIO
from threading import Thread, Event

import paho.mqtt.client as mqtt
import subprocess
import datetime
import socket
import random
import json
import time
import os

try:
    from library.raspberry import Raspberry

except Exception as e:
    pass

# Define some global variables
ID = "i"
ID_TILE = "id_tile"
VALUE = "v"
INDEX = "index"
NAME = "name"
TYPE = "type"
EDIT = "edit"
# TODO to templates

BROKER = "192.168.0.100"
PORT = 1883
USER = "username"
PASSWORD = "12345678"

HOME = "home"


# Initialise Flask
app = Flask(__name__)
socket_io = SocketIO(app)

# Initialise modules
fmng = FileManager()
werkzeug_logger = WerkzeugLogger(priority=fmng.config()["werkzeug_priority"])
auth_logger = AuthLogger(priority=fmng.config()["auth_priority"])
console_logger = ConsoleLogger(priority=fmng.config()["console_priority"])
console = Console(logger=console_logger, priority=fmng.config()["console_priority"], socket_io=socket_io)
tmng = TemplateManager(fmng=fmng, console=console)
tmng_rwr = TemplateManagerRewrite(fmng=fmng, tmng=tmng)
arduino = Arduino(console=console)
html_json = HTML_JSON()
auth = Auth(fmng=fmng, logger=auth_logger)
validator = Validator(fmng=fmng, tmng=tmng)

try:
    raspberry = Raspberry()

except Exception as e:
    console.print("This device is not a Raspberry! Some\nfunctions may not work correctly!", 1)

validate = validator.validate_jsons()
if validate is not True:
    console.print("Error in JSON due: {0}".format(validate), 2)
    exit()

check_duplicity = validator.check_duplicity_ids()
if check_duplicity is not True:
    console.print("Duplicity detected in: {0}".format(check_duplicity), 1)

# Multi-threading
mqtt_thread = Thread()
mqtt_stop = Event()

raspberry_thread = Thread()
raspberry_stop = Event()

arduino_thread = Thread()
arduino_stop = Event()


class MQTT_BROKER(Thread):
    DELAY = 2
    NAMESPACE = "/acom"

    def __init__(self):
        super(MQTT_BROKER, self).__init__()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(HOME + "/#")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        id_tile = topic.split("/")[1]
        try:
            element_id = topic.split("/")[2]

        except:
            socket_io.emit("tile", {ID: id_tile, VALUE: msg.payload.decode()},
                           namespace=self.NAMESPACE)

        else:
            arduino.write(
                html_json.to_html(json_data={ID: "bed-toggle", ID_TILE: "bed-toggle", VALUE: msg.payload.decode()}))

            socket_io.emit("slider", {ID_TILE: id_tile, ID: element_id, VALUE: msg.payload.decode()},
                           namespace=self.NAMESPACE)

            socket_io.emit("toggle", {ID_TILE: id_tile, ID: element_id, VALUE: msg.payload.decode()},
                           namespace=self.NAMESPACE)

        # self.client.disconnect()

    def run(self):
        self.client = mqtt.Client()

        try:
            self.client.connect(BROKER, 1883, 60)

        except:
            console.print("MQTT is not working. Some functions may\nnot work."
                          "Is this device Raspberry Pi? See line above", priority=2)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_forever()


class Arduino(Thread):
    """
    Arduino
    """

    DELAY = 0.1

    def __init__(self):
        super(Arduino, self).__init__()

    def arduino(self):
        raw_data = arduino.read()

        if raw_data is not None:
            data = json.loads(html_json.to_json(raw_data))

            if "alarm" in data.keys():
                # subprocess.check_output(["omxplayer", "alarm.mp3"]).decode("utf-8")
                socket_io.emit("notify", {"title": "Poplach", "message": "Senzor - postel", "type": "info"}, namespace="/acom")

    def run(self):
        """
        Sending commands
        :return:
        """

        while not arduino_stop.isSet():
            self.arduino()
            time.sleep(self.DELAY)


class Raspberry(Thread):
    """
    Raspberry
    """

    DELAY = 300
    NAMESPACE = "/acom"

    def __init__(self):
        super(Raspberry, self).__init__()

    def cpu_temp(self):
        """
        Measure CPU temp, append to Raspberry item (graph)
        :return:
        """

        data_x = str(datetime.datetime.now().strftime("%H:%M"))
        data_y = raspberry.cpu_temp()
        element_id = "modal-graph-1"
        id_tile = "raspberry-1"

        tmng.graph_rwr(id_tile=id_tile, data_x=data_x, data_y=data_y, element_id=element_id)
        socket_io.emit("graphs", {tmng.DATA_Y: data_y, tmng.DATA_X: data_x, ID: element_id, ID_TILE: id_tile},
                       namespace=self.NAMESPACE)

    def test_graph(self):
        """
        Test
        :return:
        """

        data_x = str(datetime.datetime.now().strftime("%H:%M"))
        data_y = random.randint(0, 100)
        element_id = "modal-graph-1"
        id_tile = "raspberry-1"

        tmng.graph_rwr(id_tile=id_tile, data_x=data_x, data_y=data_y, element_id=element_id)
        socket_io.emit("graphs", {tmng.DATA_Y: data_y, tmng.DATA_X: data_x, ID: element_id, ID_TILE: id_tile},
                       namespace=self.NAMESPACE)

    def run(self):
        """
        Sending commands
        :return:
        """

        while not raspberry_stop.isSet():
            # self.cpu_temp()
            time.sleep(self.DELAY)


# Error pages
@app.errorhandler(401)
def access_denied(e):
    """
    401 error
    :param e:
    :return: error page
    """

    return tmng.error_page(header="401", error=str(e))


@app.errorhandler(403)
def access_denied(e):
    """
    403 error
    :param e: event
    :return: error page
    """

    return tmng.error_page(header="403", error=str(e))


@app.errorhandler(404)
def page_not_found(e):
    """
    404 error
    :param e: event
    :return: error page
    """

    return tmng.error_page(header="404", error=str(e))


@app.errorhandler(410)
def gone(e):
    """
    410 error
    :param e: event
    :return: error page
    """

    return tmng.error_page(header="410", error=str(e))


@app.errorhandler(500)
def internal_server_error(e):
    """
    500 error
    :param e: event
    :return: error page
    """

    return tmng.error_page(header="500", error=str(e))


# Add meta
@app.after_request
def add_meta(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"

    return response


# Pages - templates
@app.route("/")
def index():
    """
    Render page
    :return:
    """

    tmng.reload_files()  # Reload HTML files

    if bool(fmng.config()["whitelist"]) is True:
        if auth.auth(ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr), browser=request.user_agent.browser,
                     system=request.user_agent.platform, header=request.user_agent):

            return tmng.index()

        else:
            abort(403)

    else:
        return tmng.index()


@app.route("/test")
def test():
    return render_template("test.html")


# Modal
@app.route("/get_modal", methods=["POST"])
def get_modal():
    """
    Get modal
    :return: modal, slider and toggle values
    """

    console.print("Loading modal...")

    id_tile = request.form[ID]
    edit = bool(int(request.form[EDIT]))

    # TODO merge names to constants
    if edit is not True:
        return json.dumps({"modal": tmng.modal(element_id=id_tile, edit=edit),
                           "sliders": tmng.get_modal_sliders(id_tile=id_tile),
                           "toggles": tmng.get_modal_toggles(id_tile=id_tile),
                           "graphs": tmng.get_modal_graphs(id_tile=id_tile)})

    else:
        return json.dumps({"modal": tmng.modal(element_id=id_tile, edit=edit),
                           "sliders": tmng.get_modal_sliders(id_tile=id_tile),
                           "toggles": tmng.get_modal_toggles(id_tile=id_tile),
                           "graphs": tmng.get_modal_graphs(id_tile=id_tile)})


@app.route("/get_modal_edit_item", methods=["POST"])
def get_modal_edit_item():
    type_of_item = request.form[TYPE]
    return json.dumps({"item": tmng.get_modal_edit_item(type_of_item=type_of_item)})


# Modal events
@app.route("/slider", methods=["POST"])
def slider():
    """
    Slider event
    :return:
    """

    json_data = request.form.to_dict(flat=True)
    element_id = request.form[ID]
    state = request.form[VALUE]
    id_tile = request.form["id_tile"]
    tmng.slider_rwr(id_tile=id_tile, state=state, element_id=element_id)
    socket_io.emit("slider", json_data, namespace="/acom")
    # socket_io.emit("notify", {"title": element_id, "message": state, "type": "info"}, namespace="/acom")
    arduino.write(html_json.to_html(json_data=json_data))

    return "ok"


@app.route("/toggle", methods=["POST"])
def toggle():
    """
    Toggle event
    :return:
    """

    json_data = request.form.to_dict(flat=True)

    element_id = request.form[ID]
    state = request.form[VALUE]
    id_tile = request.form[ID_TILE]

    socket_io.emit("toggle", json_data, namespace="/acom")
    arduino.write(html_json.to_html(json_data=json_data))

    client = mqtt.Client()
    client.username_pw_set(USER, password=PASSWORD)
    client.connect(BROKER, port=PORT)
    client.publish("{0}/{1}/{2}".format(HOME, str(id_tile), str(element_id)), state)

    if id_tile == "raspberry-1":
        if element_id == "raspberry-cpu-fan":
            raspberry.set_fan(state=int(state))

        elif element_id == "raspberry-save":
            fmng.write_file(fmng.path_join(fmng.CONFIG_DIR, fmng.CONFIG_DEVICES), fmng.devices(), True)
            socket_io.emit("notify", {"title": "Uloženo", "message": "Hodnoty byly úspěšně uloženy",
                                      "type": "success"}, namespace="/acom")

        elif element_id == "raspberry-birds":
            subprocess.check_output(["omxplayer", "birds.mp3"]).decode("utf-8")

        elif element_id == "raspberry-alarm":
            subprocess.check_output(["omxplayer", "alarm.mp3"]).decode("utf-8")

        elif element_id == "raspberry-halt":
            fmng.write_file(fmng.path_join(fmng.CONFIG_DIR, fmng.CONFIG_DEVICES), fmng.devices(), True)
            socket_io.emit("notify", {"title": "Uloženo", "message": "Hodnoty byly úspěšně uloženy",
                                      "type": "success"}, namespace="/acom")
            socket_io.emit("notify", {"title": "Kontaktuji...", "message": "Kontaktuji všechna zařízení...",
                                      "type": "info"}, namespace="/acom")
            time.sleep(3)
            socket_io.emit("notify", {"title": "Vypínání...", "message": "Nebude již možné kontrolovat zařízení",
                                      "type": "danger"}, namespace="/acom")
            subprocess.check_output(["sudo", "halt"]).decode("utf-8")

        return "ok"

    tmng.toggle_rwr(id_tile=id_tile, state=state, element_id=element_id)

    return "ok"


@app.route("/tile", methods=["POST"])
def tile():
    """
    Tile event
    :return:
    """

    json_data = request.form.to_dict(flat=True)

    element_id = request.form[ID]
    state = request.form[VALUE]

    socket_io.emit("tile", {ID: element_id, VALUE: state}, namespace="/acom")

    tmng_rwr.tile_status(state=state, element_id=element_id)

    arduino.write(html_json.to_html(json_data=json_data))
    return "ok"


# Items rewrite
@app.route("/tile_id_rwr", methods=["POST"])
def tile_id_rwr():
    json_data = request.form.to_dict(flat=True)

    element_id = request.form["tile_id"]
    new_id = request.form["new_id"]

    tmng_rwr.tile_id(element_id=element_id, new_id=new_id)

    return "ok"


@app.route("/tile_name_rwr", methods=["POST"])
def tile_name_rwr():
    json_data = request.form.to_dict(flat=True)

    element_id = request.form["tile_id"]
    new_name = request.form["new_name"]

    tmng_rwr.tile_name(element_id=element_id, new_name=new_name)

    return "ok"


@app.route("/tile_type_rwr", methods=["POST"])
def tile_type_rwr():
    """
    Tile event
    :return:
    """
    json_data = request.form.to_dict(flat=True)

    element_id = request.form["id"]  # TODO názvy do konstant
    new_type = request.form["new_type"]

    tmng_rwr.tile_type(new_type=new_type, element_id=element_id)

    arduino.write(html_json.to_html(json_data=json_data))
    return "ok"


# Modal rewrite
@app.route("/modal_item_index_rwr", methods=["POST"])
def modal_item_index_rwr():
    json_data = request.form.to_dict(flat=True)

    tile_id = request.form["id"]  # TODO názvy do konstant
    old_index = int(request.form["old_index"])
    new_index = int(request.form["new_index"])

    tmng_rwr.modal_item_index(new_index=new_index, old_index=old_index, tile_id=tile_id)

    arduino.write(html_json.to_html(json_data=json_data))
    return "ok"


# Swiper
@app.route("/swiper_title", methods=["POST"])
def swiper_title():
    index = int(request.form[INDEX])
    value = request.form[VALUE]

    tmng.title_rwr(index=index, value=value)

    return "ok"


@app.route("/append_slide", methods=["POST"])
def append_slide():
    index = int(request.form[INDEX])
    value = request.form[VALUE]
    tmng.append_slide(index=index, value=value)

    return "ok"


@app.route("/remove_slide", methods=["POST"])
def remove_slide():
    index = int(request.form[INDEX])
    tmng.remove_slide(index=index)

    return "ok"


@app.route("/tile_title", methods=["POST"])
def tile_title():
    """
    Toggle event
    :return:
    """

    element_id = request.form[ID]
    name = request.form[NAME]
    tmng.tile_title_rwr(element_id=element_id, name=name)

    return "ok"


# Client connect/disconnect
@socket_io.on("connect", namespace="/acom")
def client_connect():
    """
    Event on user connect
    :return:
    """
    # print(request.environ['SERVER_NAME'])
    # print("Base url without port", request.remote_addr)
    # print("Base url with port", request.host_url)
    console.print("Client connected")
    console.print("\t- Client IP: " + str(request.environ.get("HTTP_X_REAL_IP", request.remote_addr)))

    data = subprocess.check_output(["arp", request.environ.get("HTTP_X_REAL_IP", request.remote_addr)]).decode("utf-8")
    for i in data.split(" "):
        if ":" in i:
            console.print("\t- MAC adress: " + str(i))

    console.print("\t- Language: " + str(request.accept_languages))
    console.print("\t- Header: " + str(request.user_agent))
    console.print("\t\t- Browser: " + str(request.user_agent.browser))
    console.print("\t\t- Version: " + str(request.user_agent.version))

    # TODO Něco po připojení uživatele (asynchronní thread)


@socket_io.on("disconnect", namespace="/acom")
def client_disconnect():
    """
    Event on user discconnect
    :return:
    """

    console.print("Client disconnected")


# Multi threading
if not mqtt_thread.is_alive():
    mqtt_thread = MQTT_BROKER()
    mqtt_thread.start()

if not raspberry_thread.is_alive():
    raspberry_thread = Raspberry()
    raspberry_thread.start()

if not arduino_thread.is_alive():
    arduino_thread = Arduino()
    arduino_thread.start()

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # TODO Turn off cashing - not working
os.environ["WERKZEUG_RUN_MAIN"] = "true"  # Turn off first Werkzeug log to console


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("\033[34m\033[1mServer IP address: \033[0m" + s.getsockname()[0] + ":5000")
    s.close()

except Exception as e:
    print("\033[32m127.0.0.1")

# Run whole application
if __name__ == "__main__" and bool(fmng.config()["run"]) is True:
    app.run(host=str(fmng.config()["host"]), debug=bool(fmng.config()["debug"]))

else:
    console.print("Stopped - see config", priority=2)
