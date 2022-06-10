import requests
from flask_babel import lazy_gettext, gettext
from threading import Thread, Event, Timer
import paho.mqtt.client as mqtt
#import face_recognition
import base64
import time
import os


# TODO remove this MQTT in 11.9
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

    def __init__(self, socket_io, ip, terminal, tmng_r, tmng_rwr, refactoring):
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

        self.__terminal.protocol("MQTT", "Connected with result code {0}".format(str(rc)))

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
            self.__terminal.protocol("MQTT", "Log ({0}): {1}".format(str(level), str(buf)))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, user_data, msg):
        """
        MQTT on_message event
        :param client:
        :param user_data:
        :param msg:
        :return: None
        """

        self.__terminal.protocol("MQTT", "Received MQTT message {0} on topic {1} with qos {2} and retain flag {3}".format(
            str(msg.payload.decode("utf-8")), str(msg.topic), str(msg.qos), str(msg.retain)))


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
            self.__terminal.protocol("MQTT", "MQTT error - probably not installed mosquitto and mosquitto-clients")


class Acom:
    """
    Asynchronous communication class
    """

    def __init__(self, terminal, socket_io, ip, tmng_r, tmng_rwr, refactoring, app, sun, refresh_clients, fmng):
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
                                    tmng_rwr=self.__tmng_rwr, tmng_r=self.__tmng_r, refactoring=self.__refactoring)
            self.mqtt_thread.start()

        # if self.__fmng.config["doorbird"].getboolean("active"):
        #     if not self.doorbird_events_thread.is_alive():
        #         self.doorbird_events_thread = DoorbirdEvents(socket_io=self.__socket_io, ip=self.__ip, terminal=self.__terminal, tmng_rwr=self.__tmng_rwr, tmng_r=self.__tmng_r, refactoring=self.__refactoring, app=self.__app, doorbird=self.__doorbird, sun=self.__sun, mqtt_thread=self.mqtt_thread, refresh_clients=self.__refresh_clients)
        #         self.doorbird_events_thread.start()
        #
        #     if not self.doorbird_video_thread.is_alive():
        #         self.doorbird_video_thread = DoorbirdVideo(socket_io=self.__socket_io, ip=self.__ip, terminal=self.__terminal, tmng_rwr=self.__tmng_rwr, tmng_r=self.__tmng_r, refactoring=self.__refactoring, app=self.__app, doorbird=self.__doorbird)
        #         self.doorbird_video_thread.start()
