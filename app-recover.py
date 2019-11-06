from werkzeug.datastructures import ImmutableMultiDict
from library.template_mng import TemplateManager
from library.file_mng import FileManager
from library.html_json import HTML_JSON
from library.console import Console
from library.arduino import Arduino
from library.auth import Auth
from flask_socketio import SocketIO
from threading import Thread, Event
from flask import Flask, request, render_template
import logging
import socket
import json
import time
import subprocess

PRIORITY = [logging.DEBUG, logging.WARNING, logging.ERROR, logging.CRITICAL, logging.FATAL]
STATUS = ["OFF", "ON"]
ID = "i"
VALUE = "v"

console = Console()
fmng = FileManager()
tmng = TemplateManager(fmng=fmng, console=console)
arduino = Arduino(console=console)
html_json = HTML_JSON()
auth = Auth()

app = Flask(__name__)
socket_io = SocketIO(app)

thread = Thread()
thread_stop_event = Event()

log = logging.getLogger("werkzeug")
log.setLevel(PRIORITY[fmng.config()["flask_priority"]])

console.print(socket.gethostbyname(socket.gethostname()), priority=1)


class AsynchronousCommunication(Thread):
    """
    Asynchronous communication class
    """

    # Define some constants
    DELAY = 2
    NAMESPACE = "/acom"
    NAME = "tile"

    def __init__(self):
        """
        Init of class AsynCommunication
        """

        super(AsynchronousCommunication, self).__init__()

    def test_generator(self):
        """
        Send some test data to script
        :return:
        """

        while not thread_stop_event.isSet():
            data = arduino.read()
            if data is not None:
                console.print(data)
                console.print(html_json.to_json(data))
                socket_io.emit(self.NAME, json.loads(html_json.to_json(data)),  namespace=self.NAMESPACE)

            time.sleep(0.1)

    def run(self):
        """
        Run Asynchronous Communication
        :return:
        """

        self.test_generator()


@app.route("/")
def index():
    """
    Render page
    :return:
    """

    if auth.auth(request.environ.get("HTTP_X_REAL_IP", request.remote_addr)):
        tmng.reload_files()  # TODO only for now
        console.print("Loaded index.html")
        return tmng.index()

    else:
        return render_template("access_denied.html")


@app.route("/err")
def access_denied():
    return render_template("access_denied.html")


@app.route("/get_modal", methods=["POST"])
def get_modal():
    """
    Get modal
    :return: modal and slider values
    """

    console.print("Loaded modal")

    id_tile = request.form[ID]

    data = fmng.devices()

    sliders = {}
    for page_num, page_content in enumerate(data[tmng.ITEMS]):
        for item_num, item_content in enumerate(data[tmng.ITEMS][page_num][tmng.DATA]):
            if data[tmng.ITEMS][page_num][tmng.DATA][item_num][tmng.DATA][tmng.ID] == id_tile:
                for modal_item in item_content[tmng.MODAL]:
                    if modal_item[tmng.TYPE] == tmng.SLIDER:
                        sliders[modal_item[tmng.DATA][tmng.ID]] = modal_item[tmng.VALUE]
                break
        else:
            continue
        break

    toggles = {}
    for page_num, page_content in enumerate(data[tmng.ITEMS]):
        for item_num, item_content in enumerate(data[tmng.ITEMS][page_num][tmng.DATA]):
            if data[tmng.ITEMS][page_num][tmng.DATA][item_num][tmng.DATA][tmng.ID] == id_tile:
                for modal_item in item_content[tmng.MODAL]:
                    if modal_item[tmng.TYPE] == tmng.TOGGLE:
                        toggles[modal_item[tmng.DATA][tmng.ID]] = modal_item[tmng.VALUE]
                break
        else:
            continue
        break

    return json.dumps({"modal": tmng.complete_modal(element_id=id_tile), "sliders": sliders, "toggles": toggles})


@app.route("/slider", methods=["POST"])
def slider():
    """
    Slider event
    :return:
    """

    json_data = request.form.to_dict(flat=True)
    id = request.form[ID]
    state = request.form[VALUE]
    id_tile = request.form["id_tile"]

    data = fmng.devices()
    for page_num, page_content in enumerate(data[tmng.ITEMS]):
        for item_num, item_content in enumerate(data[tmng.ITEMS][page_num][tmng.DATA]):
            if data[tmng.ITEMS][page_num][tmng.DATA][item_num][tmng.DATA][tmng.ID] == id_tile:
                for modal_num, modal_item in enumerate(item_content[tmng.MODAL]):
                    if modal_item[tmng.TYPE] == tmng.SLIDER and modal_item[tmng.DATA][tmng.ID] == id:
                        data[tmng.ITEMS][page_num][tmng.DATA][item_num][tmng.MODAL][modal_num][tmng.VALUE] = state
                        fmng.write_file(path=fmng.path_join(fmng.CONFIG_DIR, fmng.CONFIG_DEVICES), data=data, is_json=True)

    # socket_io.emit("slider", {ID: id, VALUE: state}, namespace="/acom")
    # arduino.write(html_json.to_html(json_data=json_data))

    return "ok"


@app.route("/toggle", methods=["POST"])
def toggle():
    """
    Slider event
    :return:
    """

    json_data = request.form.to_dict(flat=True)

    id = request.form[ID]
    state = request.form[VALUE]
    id_tile = request.form["id_tile"]

    data = fmng.devices()
    for page_num, page_content in enumerate(data[tmng.ITEMS]):
        for item_num, item_content in enumerate(data[tmng.ITEMS][page_num][tmng.DATA]):
            if data[tmng.ITEMS][page_num][tmng.DATA][item_num][tmng.DATA][tmng.ID] == id_tile:
                for modal_num, modal_item in enumerate(item_content[tmng.MODAL]):
                    if modal_item[tmng.TYPE] == tmng.TOGGLE and modal_item[tmng.DATA][tmng.ID] == id:
                        data[tmng.ITEMS][page_num][tmng.DATA][item_num][tmng.MODAL][modal_num][tmng.VALUE] = state
                        fmng.write_file(path=fmng.path_join(fmng.CONFIG_DIR, fmng.CONFIG_DEVICES), data=data, is_json=True)

    # socket_io.emit("slider", {ID: id, VALUE: state}, namespace="/acom")
    # arduino.write(html_json.to_html(json_data=json_data))

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

    data = fmng.devices()
    for page_num, page_content in enumerate(data[tmng.ITEMS]):
        for item_num, item_content in enumerate(data[tmng.ITEMS][page_num][tmng.DATA]):
            if data[tmng.ITEMS][page_num][tmng.DATA][item_num][tmng.DATA][tmng.ID] == id:
                data[tmng.ITEMS][page_num][tmng.DATA][item_num][tmng.DATA][tmng.STATUS] = STATUS[int(state)]
                fmng.write_file(path=fmng.path_join(fmng.CONFIG_DIR, fmng.CONFIG_DEVICES), data=data, is_json=True)
                break
        else:
            continue

        break

    console.print(json_data)
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

    # print(request.host)

    global thread

    if not thread.isAlive():  # When Asynchronous communication is not started
        console.print("Starting Thread")

        thread = AsynchronousCommunication()
        thread.start()  # Start Asynchronous communication


@socket_io.on("disconnect", namespace="/acom")
def client_disconnect():
    """
    Event on user discconnect
    :return:
    """

    console.print("Client disconnected")


if __name__ == "__main__" and bool(fmng.config()["run"]) is True:
    app.run(host=str(fmng.config()["host"]), debug=bool(fmng.config()["debug"]))

else:
    print("Stopped - see config")  # TODO Debug
