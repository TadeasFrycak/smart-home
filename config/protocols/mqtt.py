import random
import string

from config.protocols.default import Protocol
from flask_babel import gettext
from threading import Thread

import paho.mqtt.client as mqtt
import time
import json


class MqttThread(Thread):
    """
    MQTT class
    """

    HOME_SEND = "tx"
    HOME_RECEIVE = "rx"
    HOME_WARNING = "warn"
    HOME_ERROR = "err"
    HOME_HELLO = "hello"
    HOME_DEBUG = "debug"

    HOME_GET_RECEIVE = "gr"
    HOME_GET_SEND = "gt"

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

        self.__terminal.protocol("MQTT", "Connected with result code {0}".format(str(rc)))

        self.__client.subscribe(topic=self.join_topics(self.HOME_ERROR, "#"))
        self.__client.subscribe(topic=self.join_topics(self.HOME_WARNING, "#"))
        self.__client.subscribe(topic=self.join_topics(self.HOME_HELLO, "#"))
        self.__client.subscribe(topic=self.join_topics(self.HOME_DEBUG, "#"))
        self.__client.subscribe(topic=self.join_topics(self.HOME_GET_RECEIVE, "#"))

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

        self.__terminal.protocol("MQTT", "Received MQTT message {0} on topic {1} with qos {2} and retain flag {3}".format(
            str(msg.payload.decode("utf-8"))[:30], str(msg.topic), str(msg.qos), str(msg.retain)))

        real_topic = msg.topic.split(self.SEPARATOR)
        value = msg.payload.decode("utf-8")

        header = real_topic.pop(0)
        if header == self.HOME_ERROR:
            message = json.loads(value)
            self.__general.updater.error(message["title"], message["value"])

        elif header == self.HOME_WARNING:
            message = json.loads(value)
            self.__general.updater.warning(message["title"], message["value"])

        elif header == self.HOME_HELLO:
            self.__general.updater.connection_success(" -> ".join(real_topic), value)

        elif header == self.HOME_DEBUG:
            message = json.loads(value)
            self.__general.updater.error(message["title"], message["value"])

        elif header == self.HOME_RECEIVE:
            real_topic = self.SEPARATOR.join(real_topic)

            try:
                value = json.loads(value)

            except json.decoder.JSONDecodeError:
                pass

            self.__general.update(protocol_type="mqtt", value=value, config_part={"path": real_topic})  # TODO brát z mateřské třídy, nepsat natvrdo mqtt, path

        elif header == self.HOME_GET_RECEIVE:
            send_value = None

            if len(real_topic) == 1:
                send_value = self.__general.get_tile_value(real_topic[0])

            elif len(real_topic) == 2:
                send_value = self.__general.get_item_value(real_topic[0], real_topic[1])

            real_topic = self.SEPARATOR.join(real_topic)

            self.publish(send_value, self.SEPARATOR.join([self.HOME_GET_SEND, real_topic]))

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

    def subscribe(self, topic):
        """
        MQTT subscribe
        :param topic:
        :return: None
        """

        joined = self.join_topics(self.HOME_RECEIVE, topic)

        if not self.__can_subscribe:
            self.__queue.append(joined)
            time.sleep(0.00000000000000000001)  # Required delay

        else:
            self.__client.subscribe(topic=joined)

    def unsubscribe(self, topic):
        """
        MQTT subscribe
        :param topic:
        :return: None
        """
        self.__client.unsubscribe(topic=self.join_topics(self.HOME_RECEIVE, topic))

    def publish(self, value, path):
        # TODO join topics here
        """
        MQTT publish
        :param path:
        :param value: value
        :return: None
        """

        if type(value) == bool:
            value = 1 if value else 0

        self.__client.publish(self.join_topics(self.HOME_SEND, path), str(value))

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
            self.__terminal.protocol("MQTT", "Error - probably not installed mosquitto and mosquitto-clients")


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
        path = "".join(random.choices(string.ascii_lowercase, k=2)) + "".join(random.choices(string.digits.lower(), k=4))
        return {
            self._PATH: path
        }

    def edit_config(self):
        from config.items.input import Input

        return {
            self._PATH: Input().make_object(value=self.config()[self._PATH], prepend="rx+tx/", readonly=False, button=True, label=gettext("Path")),
        }

    def add_listener_inner(self, config):
        self.thread.subscribe(config[self._PATH])

    def remove_listener_inner(self, config):
        self.thread.unsubscribe(config[self._PATH])

    def publish(self, config, value):
        self.thread.publish(value=value, path=config[self._PATH])
        # TODO QoS
        self._general.update(protocol_type=self.TYPE, value=value, config_part={"path": config[self._PATH]})
