from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, request
from random import random
from time import sleep
from threading import Thread, Event
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        while not thread_stop_event.isSet():
            socketio.emit("newstate", {"mac": "helllo"}, namespace="/test")
            sleep(self.delay)

    def run(self):
        self.randomNumberGenerator()



# Server diagnostic
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@app.route("/post", methods = ["POST"])
def get_mac():
    data = request.form["data"]
    print(data.split("<mac>")[1].split("</mac>")[0])
    wakeonlan.send_magic_packet(data.split("<mac>")[1].split("</mac>")[0])
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app)
