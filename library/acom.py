import requests
from flask_babel import lazy_gettext, gettext
from threading import Thread, Event, Timer
import paho.mqtt.client as mqtt
import face_recognition
import base64
import time
import os


class MQTT(Thread):
    """
    MQTT class
    """

    HOME_SEND = "client"
    HOME_RECEIVE = "home"
    DOORBIRD_SEND = "doorbird_client"
    DOORBIRD_RECEIVE = "doorbird_home"

    USERNAME = "home"
    PASSWORD = "xbYRJocj08YEtazIg90QEYiccembElT1"

    SEPARATOR = "/"

    def __init__(self, socket_io, ip, terminal, tmng_r, tmng_rwr, refactoring, doorbird):
        """
        Init of MQTT class
        :param socket_io: socket_io
        :param ip: current server IP
        :param terminal: terminal
        :param tmng_rwr: tmng_rwr
        """

        super().__init__()
        self.__socket_io = socket_io
        self.__terminal = terminal
        self.__ip = ip
        self.__tmng_r = tmng_r
        self.__tmng_rwr = tmng_rwr
        self.__refactoring = refactoring
        self.__doorbird = doorbird

        self.__client = None

    def join_topics(self, *argv):
        """
        Join topics
        :param argv: arguments to join
        :return: joined arguments
        """

        return self.SEPARATOR.join(list(argv))

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, user_data, flags, rc):
        """
        MQTT on_connect event
        :param client:
        :param user_data:
        :param flags:
        :param rc:
        :return: None
        """

        self.__terminal.mqtt("Connected with result code {0}".format(str(rc)))

        # Subscribing on connect means that if we lose the connection and reconnect then subscriptions will be renewed
        # self.subscribe(client=client, topic=self.join_topics(self.HOME_RECEIVE, "#"))
        self.subscribe(client=client, topic=self.join_topics(self.DOORBIRD_RECEIVE, "#"))

    def on_log(self, client, user_data, level, buf):
        """
        MQTT on_log event
        :param client:
        :param user_data:
        :param level:
        :param buf:
        :return: None
        """
        if "PINGRESP" not in str(buf) and "PINGREQ" not in str(buf):
            self.__terminal.mqtt("Log ({0}): {1}".format(str(level), str(buf)))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, user_data, msg):
        """
        MQTT on_message event
        :param client:
        :param user_data:
        :param msg:
        :return: None
        """

        self.__terminal.mqtt("Received MQTT message {0} on topic {1} with qos {2} and retain flag {3}".format(
            str(msg.payload.decode("utf-8")), str(msg.topic), str(msg.qos), str(msg.retain)))

        try:
            ids = msg.topic.split(self.SEPARATOR)
            if ids[0] == self.DOORBIRD_RECEIVE:
                if ids[1] == "open_door":
                    self.__doorbird.open_door()

        except Exception as e:
            self.__terminal.error(e)

    @staticmethod
    def subscribe(client, topic):
        """
        MQTT subscribe
        :param client:
        :param topic:
        :return: None
        """

        client.subscribe(topic=topic)

    def publish(self, tile_id=None, item_id=None, value=None):
        """
        MQTT publish
        :param tile_id: tile ID
        :param item_id: item ID
        :param value: value
        :return: None
        """

        if item_id is not None:
            self.__client.publish(self.join_topics(self.HOME_SEND, tile_id, item_id), str(value))

        else:
            self.__client.publish(self.join_topics(self.HOME_SEND, tile_id), str(value))

    def publish_android(self, ip):
        """
        MQTT publish
        :param ip: IP
        :return: None
        """
        self.__client.publish("android_settings", str(ip))

    def publish_doorbird(self, event, image):
        """
        MQTT publish
        :param event: event type
        :param image: image data
        :return: None
        """

        self.__client.publish(self.join_topics(self.DOORBIRD_SEND, event), image)

    def run(self):
        """
        MQTT run
        :return: None
        """
        try:
            self.__client = mqtt.Client()
            self.__client.on_connect = self.on_connect
            self.__client.on_message = self.on_message
            self.__client.on_log = self.on_log

            self.__client.username_pw_set(username=self.USERNAME, password=self.PASSWORD)
            self.__client.connect("127.0.0.1", 1883, 60)

            # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
            # Other loop*() functions are available that give a threaded interface and a manual interface.
            self.__client.loop_forever()
        except ConnectionRefusedError:
            self.__terminal.mqtt("MQTT error - probably not installed mosquitto and mosquitto-clients")


class DoorbirdEvents(Thread):
    KNOWN_DIR = "doorbird/known"

    def __init__(self, socket_io, ip, terminal, tmng_r, tmng_rwr, refactoring, app, doorbird, sun, mqtt_thread, refresh_clients):
        super().__init__()
        self.__socket_io = socket_io
        self.__terminal = terminal
        self.__ip = ip
        self.__tmng_r = tmng_r
        self.__tmng_rwr = tmng_rwr
        self.__refactoring = refactoring
        self.__app = app
        self.__doorbird = doorbird
        self.__sun = sun
        self.__mqtt = mqtt_thread
        self.__refresh_clients = refresh_clients

        self.__client = None

        self.__known_faces = {}

    def make_known_faces(self):
        # For every file in dir
        for num, file in enumerate(os.listdir(self.KNOWN_DIR)):
            # Validation, if file is really image file
            if file.endswith(".jpg"):
                picture = face_recognition.load_image_file(os.path.join(self.KNOWN_DIR, file))
                # Protection [0] - in the photo must be only one person
                encoding = face_recognition.face_encodings(picture)[0]

                self.__known_faces[os.path.splitext(file)[0]] = encoding

    def is_known(self, file_path):
        unknown_picture = face_recognition.load_image_file(file_path)
        try:
            unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]  # TODO vzít oba dva z fotky, pokud tam jsou
        except IndexError:
            return False

        results = face_recognition.compare_faces(list(self.__known_faces.values()), unknown_face_encoding)

        return True in results

    def run(self):
        self.make_known_faces()  # TODO save this to temp dir
        self.__refresh_clients.doorbird()
        while True:
            try:
                response = self.__doorbird.monitor()

                for line in response.iter_lines():
                    content = line.decode().split(":")
                    if "doorbell" == content[0] and content[1] == "H":
                        self.__mqtt.publish_doorbird(content[0], self.__doorbird.live_image(resolution="VGA", without_header=True))

                        self.__socket_io.emit("notify", {"title": gettext("Doorbell"),
                                                         "message": gettext("Someone ring on the doorbell!"),
                                                         "type": "info",
                                                         "delay": 5000}, namespace=self.__app.config["SOCKETIO_NAMESPACE"],
                                              broadcast=True)

                        self.__doorbird.take_photo(content[0])

                        if self.is_known(self.__doorbird.take_photo("temp", "VGA")):
                            self.__doorbird.open_door()

                        self.__refresh_clients.doorbird()
                        self.__socket_io.emit("doorbird_event", broadcast=True,
                                              namespace=self.__app.config["SOCKETIO_NAMESPACE"])

                    elif "motionsensor" == content[0] and content[1] == "H":
                        self.__socket_io.emit("notify", {"title": gettext("Doorbell"),
                                                         "message": gettext("Someone moved in front of the doorbell!"),
                                                         "type": "info",
                                                         "delay": 5000}, namespace=self.__app.config["SOCKETIO_NAMESPACE"],
                                              broadcast=True)

                    else:
                        continue
            except requests.exceptions.ChunkedEncodingError as e:
                print("====================================")
                print("monitor.cgi - ChunkedEncodingError")
                print("---------------")

                print(e)

                print("---------------")
                print("monitor.cgi - ChunkedEncodingError")
                print("====================================")
                time.sleep(1)
                continue
            except requests.exceptions.ConnectionError as e:
                print("====================================")
                print("monitor.cgi - ConnectionError")
                print("---------------")

                print(e)

                print("---------------")
                print("monitor.cgi - ConnectionError")
                print("====================================")
                time.sleep(1)
                continue


class DoorbirdVideo(Thread):
    def __init__(self, socket_io, ip, terminal, tmng_r, tmng_rwr, refactoring, app, doorbird):
        super().__init__()
        self.__socket_io = socket_io
        self.__terminal = terminal
        self.__ip = ip
        self.__tmng_r = tmng_r
        self.__tmng_rwr = tmng_rwr
        self.__refactoring = refactoring
        self.__app = app
        self.__doorbird = doorbird

        self.__client = None

    def run(self):
        last_time = time.time()
        framerate = 0
        frames = 0

        while True:
            try:
                response = self.__doorbird.video()
                for line in response.iter_lines(delimiter="--my-boundary".encode("iso-8859-1")):
                    frames += 1
                    try:
                        without_header = line.decode("iso-8859-1").split("\r\n\r\n")[1].encode("iso-8859-1")
                        base64_encoded = base64.b64encode(without_header).decode("utf-8")
                        content = self.__doorbird.image_header(base64_encoded)

                    except IndexError:  # Empty
                        continue

                    current_time = time.time()
                    if current_time - last_time > 1:
                        last_time = current_time
                        framerate = frames
                        frames = 0
                    self.__socket_io.emit("doorbird_live_image", {"image": content, "framerate": framerate}, broadcast=True, namespace="/com")
            except requests.exceptions.ChunkedEncodingError as e:
                print("====================================")
                print("video.cgi - ChunkedEncodingError")
                print("---------------")

                print(e)

                print("---------------")
                print("video.cgi - ChunkedEncodingError")
                print("====================================")
                time.sleep(1)
                continue
            except requests.exceptions.ConnectionError as e:
                print("====================================")
                print("video.cgi - ConnectionError")
                print("---------------")

                print(e)

                print("---------------")
                print("video.cgi - ConnectionError")
                print("====================================")
                time.sleep(1)
                continue


class Acom:
    """
    Asynchronous communication class
    """

    def __init__(self, terminal, socket_io, ip, tmng_r, tmng_rwr, refactoring, app, doorbird, sun, refresh_clients, fmng):
        """
        Init of asynchronous communication class
        :param terminal: terminal
        :param socket_io: socket_io
        :param ip: server IP
        :param tmng_rwr: tmng_rwr
        """

        self.__socket_io = socket_io
        self.__ip = ip
        self.__terminal = terminal
        self.__tmng_r = tmng_r
        self.__tmng_rwr = tmng_rwr
        self.__refactoring = refactoring
        self.__app = app
        self.__doorbird = doorbird
        self.__sun = sun
        self.__refresh_clients = refresh_clients
        self.__fmng = fmng

        self.mqtt_thread = Thread()
        self.mqtt_stop = Event()

        self.doorbird_events_thread = Thread()
        self.doorbird_events_stop = Event()

        self.doorbird_video_thread = Thread()
        self.doorbird_video_stop = Event()

    def run(self):
        """
        Start
        :return: None
        """

        if not self.mqtt_thread.is_alive():
            self.mqtt_thread = MQTT(socket_io=self.__socket_io, ip=self.__ip, terminal=self.__terminal,
                                    tmng_rwr=self.__tmng_rwr, tmng_r=self.__tmng_r, refactoring=self.__refactoring, doorbird=self.__doorbird)
            self.mqtt_thread.start()

        if self.__fmng.config["doorbird"].getboolean("active"):
            if not self.doorbird_events_thread.is_alive():
                self.doorbird_events_thread = DoorbirdEvents(socket_io=self.__socket_io, ip=self.__ip, terminal=self.__terminal, tmng_rwr=self.__tmng_rwr, tmng_r=self.__tmng_r, refactoring=self.__refactoring, app=self.__app, doorbird=self.__doorbird, sun=self.__sun, mqtt_thread=self.mqtt_thread, refresh_clients=self.__refresh_clients)
                self.doorbird_events_thread.start()

            if not self.doorbird_video_thread.is_alive():
                self.doorbird_video_thread = DoorbirdVideo(socket_io=self.__socket_io, ip=self.__ip, terminal=self.__terminal, tmng_rwr=self.__tmng_rwr, tmng_r=self.__tmng_r, refactoring=self.__refactoring, app=self.__app, doorbird=self.__doorbird)
                self.doorbird_video_thread.start()
