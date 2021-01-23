import json
import time

from config.protocols.default import Protocol
from threading import Thread
from flask_babel import gettext
import paho.mqtt.client as mqtt


class MqttThread(Thread):
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

    def __init__(self, terminal, general):
        """
        Init of MQTT class
        :param terminal: terminal
        """

        super().__init__()
        self.__terminal = terminal
        self.__general = general

        self.__client = None

        self.__can_subscribe = False
        self.__queue = []

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

        self.__can_subscribe = True
        for topic in self.__queue:
            self.__client.subscribe(topic=topic)
        # Subscribing on connect means that if we lose the connection and reconnect then subscriptions will be renewed
        # self.subscribe(client=client, topic=self.join_topics(self.HOME_RECEIVE, "#"))

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

        # ids = msg.topic.split(self.SEPARATOR)
        # ids.remove(self.HOME_RECEIVE)

        try:
            value = int(msg.payload.decode("utf-8"))

        except ValueError:
            try:
                value = float(msg.payload.decode("utf-8"))
            except ValueError:
                if msg.payload.decode("utf-8").lower() == "false" or msg.payload.decode("utf-8").lower() == "true":
                    value = msg.payload.decode("utf-8").lower() == "true"
                else:
                    try:
                        value = json.loads(msg.payload.decode("utf-8"))

                    except json.decoder.JSONDecodeError:
                        value = msg.payload.decode("utf-8")
        self.__general.update(protocol_type="mqtt", value=value, config_part={"path": msg.topic})  # TODO brát z mateřské třídy, nepsat natvrdo mqtt, path

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

    def subscribe(self, topic):
        """
        MQTT subscribe
        :param topic:
        :return: None
        """

        if not self.__can_subscribe:
            self.__queue.append(topic)
        else:
            # self.__client.subscribe(topic=self.join_topics(self.HOME_RECEIVE, topic))
            self.__client.subscribe(topic=topic)  # TODO ochrana, udělat jen client na odchozí a home na příchozéí

    def unsubscribe(self, topic):
        """
        MQTT subscribe
        :param topic:
        :return: None
        """

        # self.__client.unsubscribe(topic=self.join_topics(self.HOME_RECEIVE, topic))
        self.__client.unsubscribe(topic=topic)

    def publish(self, value, path):
        """
        MQTT publish
        :param path:
        :param value: value
        :return: None
        """

        self.__client.publish(path, str(value))

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


class MQTT(Protocol):

    TYPE = "mqtt"
    VISIBLE = True
    NAME = gettext("MQTT")

    __HOME = "home"

    def __init__(self, terminal, update):
        super().__init__(terminal, update)

        if not self.thread.is_alive():
            self.thread = MqttThread(terminal=self._terminal, general=self._general)
            self.thread.start()

    def config(self):
        path = f"{self.__HOME}/test"
        return {
            self._PATH: path
        }

    def edit_config(self):
        from config.items.input import Input

        return {
            self._PATH: Input().make_object(value=self.config()[self._PATH], prepend="home", readonly=False, button=True, label=gettext("Path")),
        }

    def add_listener_inner(self, config):
        self.thread.subscribe(config[self._PATH])

    def remove_listener_inner(self, config):
        self.thread.unsubscribe(config[self._PATH])

    def publish(self, config, value):
        self.thread.publish(value=value, path=config[self._PATH])
