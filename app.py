from library.logger import WerkzeugLogger, AuthLogger
from library.template_mng import TemplateManager
from library.file_mng import FileManager
from library.html_json import HTML_JSON
from library.console import Console
from library.arduino import Arduino
from library.auth import Auth

from flask import Flask, request, render_template, abort
from flask_socketio import SocketIO
from threading import Thread, Event

import paho.mqtt.client as mqtt
import subprocess
import datetime
import random
import json
import time

try:
    from library.raspberry import Raspberry

except Exception as e:
    pass

# Define some global variables
ID = "i"
ID_TILE = "id_tile"
VALUE = "v"
BROKER = "192.168.0.100"
PORT = 1883
USER = "username"
PASSWORD = "12345678"

HOME = "home"


# Initialise Flask
app = Flask(__name__)
socket_io = SocketIO(app)

# Initialise modules
werkzeug_logger = WerkzeugLogger()
auth_logger = AuthLogger()
console = Console(socket_io=socket_io)
fmng = FileManager()
tmng = TemplateManager(fmng=fmng, console=console)
arduino = Arduino(console=console)
html_json = HTML_JSON()
auth = Auth(fmng=fmng, logger=auth_logger)

try:
    raspberry = Raspberry()

except Exception as e:
    console.print("This device is not a Raspberry! Some functions may not work correctly!", 2)

validate = fmng.validate_jsons()
if validate is not True:
    console.print("Error in JSON due: {0}".format(validate), 3)

check_duplicity = tmng.check_duplicity_ids()
if check_duplicity is not True:
    console.print("Duplicity detected in: {0}".format(check_duplicity), 2)

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
            console.print("MQTT is not working. Some functions may not work", priority=3)

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


@app.route("/")
def index():
    """
    Render page
    :return:
    """

    if bool(fmng.config()["whitelist"]) is True:
        if auth.auth(ip=request.environ.get("HTTP_X_REAL_IP", request.remote_addr), browser=request.user_agent.browser,
                     system=request.user_agent.platform, header=request.user_agent):

            return tmng.index()

        else:
            abort(403)

    else:
        return tmng.index()


@app.route("/get_modal", methods=["POST"])
def get_modal():
    """
    Get modal
    :return: modal, slider and toggle values
    """

    console.print("Loading modal...")

    id_tile = request.form[ID]

    return json.dumps({"modal": tmng.complete_modal(element_id=id_tile), "sliders": tmng.get_sliders(id_tile=id_tile),
                       "toggles": tmng.get_toggles(id_tile=id_tile), "graphs": tmng.get_graphs(id_tile=id_tile)})


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
    id_tile = request.form["id_tile"]

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

    id = request.form[ID]
    state = request.form[VALUE]

    socket_io.emit("tile", {ID: id, VALUE: state}, namespace="/acom")

    tmng.tile_rwr(state=state, element_id=id)

    arduino.write(html_json.to_html(json_data=json_data))
    return "ok"


@socket_io.on("connect", namespace="/acom")
def client_connect():
    """
    Event on user connect
    :return:
    """

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

# Run whole application
if __name__ == "__main__" and bool(fmng.config()["run"]) is True:
    app.run(host=str(fmng.config()["host"]), debug=bool(fmng.config()["debug"]))
    print("AGDFJHSDGFJGSDFHSADFGKDSJFGKJGHASDKJFGHSDFJKHSDGFKJHSDGFKAJSGHFKSJHFGKASDJFGSKJFGSDJKFGJASDFH")

else:
    console.print("Stopped - see config", priority=3)
