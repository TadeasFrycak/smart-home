from flask import Flask, render_template, url_for, copy_current_request_context, request
from console_interact import PythonConsole
from flask_socketio import SocketIO, emit
from arduino import Arduino
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

try:    
    pythonConsole.introduction()

except Exception as e:
    pythonConsole.error(e)
    input()

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
        pass
        # TODO NAMESPACE i v disconnect a connect
        
        #while not thread_stop_event.isSet():
        #    socketio.emit(self.NAME, {"type": "console", "status": "error", "message": "Just a test"},
        #                   namespace=self.NAMESPACE)

        #    time.sleep(self.DELAY)

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


@app.route("/post", methods=["POST"])
def receive():
    d = request.form["data"]
    pythonConsole.debug(d)
     
    if d.split("<value>")[1].split("</value>")[0] == "100":
        for i in range(256):
            i = str(i)
            arduino.write("<type>rgbw_slider</type> <name>Postel</name> <id>bed</id> <icon-id>1</icon-id> <value>0</value> <l>"+i+"</l> <r>"+i+"</r> <u>"+i+"</u> <d>"+i+"</d>")
    
    else:
        #for i in range(255,-1,-1):
        #    i = str(i)
        #    arduino.write("<type>rgbw_slider</type> <name>Postel</name> <id>bed</id> <icon-id>1</icon-id> <value>0</value> <l>"+i+"</l> <r>"+i+"</r> <u>"+i+"</u> <d>"+i+"</d>")        
        
        arduino.write(d)

    return "ok"


@app.route("/")
def index():
    """
    Render index.html file
    :return: template to render
    """
    # supported_languages = ["en", "cs", "sk", "ru"]
    # lang = request.accept_languages.best_match(supported_languages)
    # print(request.accept_languages)
    # print(lang)
    # print(request.headers)
    
    return render_template("index.html")


@socketio.on("connect", namespace="/test")
def client_connect():
    """
    Event on user connect
    :return:
    """

    pythonConsole.debug("Client connected")
    pythonConsole.debug("\t- Client IP: " + str(request.environ.get("HTTP_X_REAL_IP", request.remote_addr)))
    pythonConsole.debug("\t- Language: " + str(request.accept_languages))
    pythonConsole.debug("\t- Header: " + str(request.user_agent))
    pythonConsole.debug("\t\t- Browser: " + str(request.user_agent.browser))
    pythonConsole.debug("\t\t- Version: " + str(request.user_agent.version))
    pythonConsole.debug("\t\t- Platform: " + str(request.user_agent.platform))
    print(request.host)
    
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

