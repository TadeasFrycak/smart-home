from flask import Flask, render_template, url_for, copy_current_request_context, request
from flask_socketio import SocketIO, emit
from threading import Thread, Event
import subprocess
import os.path
import random
import json
import glob
import time
import os

SEPARATORS = (",", ":")
IMG_PATH = "static/Img"
IMG_BCG = "bcg"

CURRENT_FOLDER = os.getcwd()
CURRENT_FILE = __file__

current_version = CURRENT_FOLDER.split("IoT")
current_version = current_version[len(current_version)-1].strip()
print("------------------------------------------------------------")
print("Smart Home - App")
print("Version: " + current_version)
print("Authors: Filip Szkandera, Tadeáš Fryčák")
print("IP: 127.0.0.1")
print("Port: 5000")
print("Working directory: ")
print("  - Path: " + CURRENT_FOLDER)
print("  - Created: %s" % time.ctime(os.path.getctime(CURRENT_FOLDER)))
print("  - Last modified: %s" % time.ctime(os.path.getmtime(CURRENT_FOLDER)))
print("Flask Python file:")
print("  - Path: " + CURRENT_FILE)
print("  - Created: %s" % time.ctime(os.path.getctime(CURRENT_FILE)))
print("  - Last modified: %s" % time.ctime(os.path.getmtime(CURRENT_FILE)))
print("------------------------------------------------------------")

# Create app
app = Flask(__name__)
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()


class AsynCommunication(Thread):
    """
    AsynCommunication class
    """
    
    # Define some constants
    DELAY = 10
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
            socketio.emit(self.NAME, {"mac": "helllo"}, namespace=self.NAMESPACE)  # Send message
            time.sleep(self.DELAY)  # Sleep

    def run(self):
        """
        Run Asyn Communication
        :return:
        """
        
        self.test_generator()


@app.route("/change_item_state/<data>")
def change_item_state(data):
    """
    Change item state
    :data: data
    :return: JSON
    """
    
    return json.dumps({"status": random.choice(["ok", "not ok", "pending"]), "debug_data": json.loads(data)}, separators=SEPARATORS)


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
    
    return json.dumps({"status": "ok", "images": backgrounds}, separators=SEPARATORS)


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

    print("Client connected")
    global thread

    if not thread.isAlive():  # When AsynCommunication is not started
        print("Starting Thread")
        
        thread = AsynCommunication()
        thread.start()  # Start AsynCommunication


@socketio.on("disconnect", namespace="/test")
def client_disconnect():
    """
    Event on user discconnect
    :return:
    """
    
    print("Client disconnected")

if __name__ == "__main__":
    socketio.run(app)
