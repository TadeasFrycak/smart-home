from flask import Flask, render_template, url_for, copy_current_request_context, request
from templates.html_to_json_parser import HTMLtoJSONParser
from templates.console_interact import PythonConsole
from flask_socketio import SocketIO, emit
from templates.arduino import Arduino
from threading import Thread, Event
import os.path
import random
import json
import glob
import os

SEPARATORS = (",", ":")
IMG_PATH = "static/Img"
IMG_BCG = "bcg"
ICON = "icon"

pythonConsole = PythonConsole()
pythonConsole.introduction()

# Create app
app = Flask(__name__)
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()

arduino = Arduino(console_log=pythonConsole)

data = [0, "0", "0", "0"]


class AsynCommunication(Thread):
    """
    Asynchronous communication class
    """
    
    # Define some constants
    DELAY = 2
    NAMESPACE = "/test"
    NAME = "newstate"
    
    def __init__(self):
        """
        Init of class AsynCommunication
        """
        
        super(AsynCommunication, self).__init__()

    def test_generator(self):
        """
        Send some test data to script
        :return:
        """
        
        while not thread_stop_event.isSet():
            socketio.emit(self.NAME, {"type": "console", "status": "error", "message": "Just a test"},
                           namespace=self.NAMESPACE)
            # socketio.emit(self.NAME, {"type": "console", "status": "error", "message": "Just a test"},
            #               namespace=self.NAMESPACE)
            # data = arduino.write_read(data="g1;?")
            #
            # if data is not False:
            #    print(data)
            #    socketio.emit(self.NAME, {"type": "temperature_sensor", "id": data.split(";")[0],
            #                              "value": data.split(";")[1], "color": "red"}, namespace=self.NAMESPACE)
            #
            # f = open("static/device-config.txt", "r")
            # content = f.readlines()
            # f.close()
            #
            # for i in content:
            #    if ";" not in i and i.strip() != "" and "<page>" not in i:
            #        if i.split("<type>")[1].split("</type>")[0] == "gauge":
            #            before_rand = data[0]
            #            rand = random.randint(0,255)
            #            data[0] = rand
            #            for j in range(before_rand, rand):
            #                print(j)
            #                socketio.emit(self.NAME, {"type": "temperature_sensor",
            #                                          "id": i.split("<id>")[1].split("</id>")[0], "value": j,
            #                                          "color": "red"}, namespace=self.NAMESPACE)
            #               "color": random.choice(["red", "yellow", "green", "blue", "black", "white", "orange",
            #                                       "gold", "silver", "pink", "purple", "gray", "brown"])},
            #                                      namespace=self.NAMESPACE)  # Send message
            #                time.sleep(0.01)
            #            time.sleep(self.DELAY)  # Sleep

    def run(self):
        """
        Run Asynchronous Communication
        :return:
        """
        
        self.test_generator()


@app.route("/get_background_images")
def get_background_images():
    """
    Get background images
    :return: background images
    """

    backgrounds = []
    
    os.chdir(IMG_PATH)

    for file in glob.glob("*.*"):
        if IMG_BCG in file:
            backgrounds.append("../" + IMG_PATH + "/" + file)
            
    os.chdir("../../")
    
    return json.dumps({"status": "ok", "images": backgrounds, "random_image": random.choice(backgrounds)},
                      separators=SEPARATORS)


@app.route("/get_icons")
def get_icons():
    """
    Get background images
    :return: background images
    """

    icons = {}
    
    os.chdir(IMG_PATH)

    for file in glob.glob("*.*"):
        if ICON in file:
            icons["icon" + file.split("-")[1]] = "../" + IMG_PATH + "/" + file
            
    os.chdir("../../")
    
    return json.dumps({"status": "ok", "icons": icons}, separators=SEPARATORS)


# @app.route("/html_json")
# def html_json():
#    return HTMLtoJSONParser.to_json(data[0])


@app.route("/post", methods=["POST"])
def get_mac():
    pythonConsole.debug(request.form["data"])

    return "ok"


@app.route("/")
def index():
    """
    Render index.html file
    :return: template to render
    """
    
    return render_template("index.html")


@socketio.on("connect", namespace="/test")
def client_connect():
    """
    Event on user connect
    :return:
    """

    pythonConsole.debug("Client connected")
    pythonConsole.print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    global thread

    if not thread.isAlive():  # When Asynchronous communication is not started
        pythonConsole.debug("Starting Thread")
        
        thread = AsynCommunication()
        thread.start()  # Start Asynchronous communication


@socketio.on("disconnect", namespace="/test")
def client_disconnect():
    """
    Event on user discconnect
    :return:
    """
    
    pythonConsole.debug("Client disconnected")


# if __name__ == "__main__":
#    socketio.run(app)
