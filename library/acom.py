import json
import shutil
import time
from threading import Thread, Event, Timer
from flask import render_template
import paho.mqtt.client as mqtt
import requests
from flask_babel import lazy_gettext, gettext
from flask_login import current_user


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
        self.subscribe(client=client, topic=self.join_topics(self.HOME_RECEIVE, "#"))
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
            else:
                ids.remove(self.HOME_RECEIVE)

                tile_id = ids[0]
                try:
                    value = int(msg.payload.decode("utf-8"))

                except Exception as e:
                    try:
                        value = float(msg.payload.decode("utf-8"))

                    except Exception as e:
                        try:
                            value = json.loads(msg.payload.decode("utf-8"))

                        except Exception as e2:
                            value = msg.payload.decode("utf-8")

                socketio_value = value

                if len(ids) > 1:
                    item_id = ids[1]
                    self.__tmng_rwr.modal_toggle(tile_id=tile_id, item_id=item_id, new_value=value)
                    self.__socket_io.emit("modal_item_value_result", {"tile_id": tile_id, "value": value, "id": item_id}, namespace="/com", broadcast=True)

                else:
                    if self.__tmng_r.get_tile_type(tile_id=tile_id) == "value":
                        value = value.copy()
                        value["time"] = time.time()

                        socketio_value = value.copy()
                        socketio_value["ago"] = self.__refactoring.get_time_ago(socketio_value["time"])

                    self.__tmng_rwr.tile_value(new_value=value, tile_id=tile_id)
                    self.__socket_io.emit("tile_value_result", {"tile_id": tile_id, "value": socketio_value}, namespace="/com", broadcast=True)

        except Exception as e:
            self.__terminal.error("MQTT", e)

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
        print(self.join_topics(self.DOORBIRD_SEND, event), image)
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
            self.__client.connect(self.__ip, 1883, 60)

            # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
            # Other loop*() functions are available that give a threaded interface and a manual interface.
            self.__client.loop_forever()
        except ConnectionRefusedError:
            self.__terminal.mqtt("MQTT error - probably not installed mosquitto and mosquitto-clients")


class DoorbirdEvents(Thread):
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

    def run(self):
        while True:
            self.__refresh_clients.doorbird()
            response = self.__doorbird.monitor()

            for line in response.iter_lines():
                content = line.decode().split(":")
                if "doorbell" == content[0] and content[1] == "H":
                    self.__socket_io.emit("notify", {"title": gettext("Doorbell"),
                                                     "message": gettext("Someone ring on the doorbell!"),
                                                     "type": "info",
                                                     "delay": 5000}, namespace=self.__app.config["SOCKETIO_NAMESPACE"],
                                          broadcast=True)
                elif "motionsensor" == content[0] and content[1] == "H":
                    self.__socket_io.emit("notify", {"title": gettext("Doorbell"),
                                                     "message": gettext("Someone moved in front of the doorbell!"),
                                                     "type": "info",
                                                     "delay": 5000}, namespace=self.__app.config["SOCKETIO_NAMESPACE"],
                                          broadcast=True)
                else:
                    continue
                self.__refresh_clients.doorbird()
                self.__doorbird.take_photo(content[0])
                self.__mqtt.publish_doorbird(content[0], "1")  # self.__doorbird.live_image(resolution="VGA"))
                self.__socket_io.emit("doorbird_event", broadcast=True, namespace=self.__app.config["SOCKETIO_NAMESPACE"])


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
            response = self.__doorbird.live_image(resolution="vga")
            frames += 1

            current_time = time.time()
            if current_time - last_time > 1:
                last_time = current_time
                framerate = frames
                frames = 0

            self.__socket_io.emit("doorbird_live_image", {"image": response, "framerate": framerate}, broadcast=True, namespace="/com")


class Acom:
    """
    Asynchronous communication class
    """

    def __init__(self, terminal, socket_io, ip, tmng_r, tmng_rwr, refactoring, app, doorbird, sun, refresh_clients):
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

        if not self.doorbird_events_thread.is_alive():
            self.doorbird_events_thread = DoorbirdEvents(socket_io=self.__socket_io, ip=self.__ip, terminal=self.__terminal, tmng_rwr=self.__tmng_rwr, tmng_r=self.__tmng_r, refactoring=self.__refactoring, app=self.__app, doorbird=self.__doorbird, sun=self.__sun, mqtt_thread=self.mqtt_thread, refresh_clients=self.__refresh_clients)
            self.doorbird_events_thread.start()

        if not self.doorbird_video_thread.is_alive():
            self.doorbird_video_thread = DoorbirdVideo(socket_io=self.__socket_io, ip=self.__ip, terminal=self.__terminal, tmng_rwr=self.__tmng_rwr, tmng_r=self.__tmng_r, refactoring=self.__refactoring, app=self.__app, doorbird=self.__doorbird)
            self.doorbird_video_thread.start()
