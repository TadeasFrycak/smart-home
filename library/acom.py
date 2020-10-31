import json
import time
from threading import Thread, Event, Timer
import paho.mqtt.client as mqtt


class MQTT(Thread):
    """
    MQTT class
    """

    HOME_SEND = "client"
    HOME_RECEIVE = "home"

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

        self.__terminal.mqtt("Connected with result code {0}".format(str(rc)))

        # Subscribing on connect means that if we lose the connection and reconnect then subscriptions will be renewed
        self.subscribe(client=client, topic=self.join_topics(self.HOME_RECEIVE, "#"))

    def on_log(self, client, user_data, level, buf):
        """
        MQTT on_log event
        :param client:
        :param user_data:
        :param level:
        :param buf:
        :return: None
        """

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

        ids = msg.topic.split(self.SEPARATOR)
        ids.remove(self.HOME_RECEIVE)

        tile_id = ids[0]
        try:
            value = int(msg.payload.decode("utf-8"))

        except Exception as e:
            try:
                value = json.loads(msg.payload.decode("utf-8"))

            except Exception as e2:
                value = msg.payload.decode("utf-8")

        socketio_value = value

        self.__terminal.mqtt("Received MQTT message {0} on topic {1} with qos {2} and retain flag {3}".format(
            str(msg.payload.decode("utf-8")), str(msg.topic), str(msg.qos), str(msg.retain)))

        if len(ids) > 1:
            item_id = ids[1]
            self.__tmng_rwr.modal_toggle(tile_id=tile_id, item_id=item_id, new_value=value)
            self.__socket_io.emit("modal_toggle_result", {"tile_id": tile_id, "value": value, "id": item_id}, namespace="/com", broadcast=True)

        else:
            if self.__tmng_r.get_tile_type(tile_id=tile_id) == "value":
                value = value.copy()
                value["time"] = time.time()

                socketio_value = value.copy()
                socketio_value["ago"] = self.__refactoring.get_time_ago(socketio_value["time"])

            self.__tmng_rwr.tile_value(new_value=value, tile_id=tile_id)
            self.__socket_io.emit("tile_value_result", {"tile_id": tile_id, "value": socketio_value}, namespace="/com", broadcast=True)

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
            self.__client.connect(self.__ip, 1883, 60)

            # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
            # Other loop*() functions are available that give a threaded interface and a manual interface.
            self.__client.loop_forever()
        except ConnectionRefusedError:
            self.__terminal.mqtt("MQTT error - probably not installed mosquitto and mosquitto-clients")


class Acom:
    """
    Asynchronous communication class
    """

    def __init__(self, terminal, socket_io, ip, tmng_r, tmng_rwr, refactoring):
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
        self.mqtt_thread = Thread()
        self.mqtt_stop = Event()

    def run(self):
        """
        Start
        :return: None
        """

        if not self.mqtt_thread.is_alive():
            self.mqtt_thread = MQTT(socket_io=self.__socket_io, ip=self.__ip, terminal=self.__terminal,
                                    tmng_rwr=self.__tmng_rwr, tmng_r=self.__tmng_r, refactoring=self.__refactoring)
            self.mqtt_thread.start()
