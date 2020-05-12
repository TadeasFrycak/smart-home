from threading import Thread, Event
import paho.mqtt.client as mqtt


class MQTT(Thread):
    HOME = "home"

    USERNAME = "home"
    PASSWORD = "xbYRJocj08YEtazIg90QEYiccembElT1"

    SEPARATOR = "/"

    def __init__(self, socket_io, ip, console, tmng_rwr):
        super().__init__()
        self.__socket_io = socket_io
        self.__console = console
        self.__ip = ip
        self.__tmng_rwr = tmng_rwr

        self.__client = None

    def join_topics(self, *argv):
        return self.SEPARATOR.join(list(argv))

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, user_data, flags, rc):
        self.__console.print("MQTT connected with result code {0}".format(str(rc)), 0)

        # Subscribing on connect means that if we lose the connection and reconnect then subscriptions will be renewed
        self.subscribe(client=client, topic=self.join_topics(self.HOME, "#"))

    def on_log(self, client, user_data, level, buf):
        self.__console.print("MQTT log on level {0} and buffer {1}".format(str(level), str(buf)), 0)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, user_data, msg):
        ids = msg.topic.split(self.SEPARATOR)
        ids.remove(self.HOME)

        tile_id = ids[0]
        value = int(msg.payload.decode("utf-8"))

        self.__console.print("Received MQTT message {0} on topic {1} with qos {2} and retain flag {3}".format(
            str(msg.payload.decode("utf-8")), str(msg.topic), str(msg.qos), str(msg.retain)))

        if len(ids) > 1:
            item_id = ids[1]
            self.__tmng_rwr.modal_toggle(tile_id=tile_id, item_id=item_id, new_value=value)
            self.__socket_io.emit("toggle", {"tile_id": tile_id, "value": value, "id": item_id}, namespace="/com")

        else:
            self.__tmng_rwr.tile_value(new_value=value, tile_id=tile_id)
            self.__socket_io.emit("tile", {"id": tile_id, "value": value}, namespace="/com")

    @staticmethod
    def subscribe(client, topic):
        client.subscribe(topic=topic)

    def publish(self, tile_id=None, item_id=None, value=None):
        if item_id is not None:
            self.__client.publish(self.join_topics(self.HOME, tile_id, item_id), str(value))

        else:
            self.__client.publish(self.join_topics(self.HOME, tile_id), str(value))

    def run(self):
        self.__client = mqtt.Client()
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message
        self.__client.on_log = self.on_log

        self.__client.username_pw_set(username=self.USERNAME, password=self.PASSWORD)
        self.__client.connect(self.__ip, 1883, 60)

        # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a manual interface.
        self.__client.loop_forever()


class Acom:
    """
    Asynchronous communication class
    """

    def __init__(self, console, socket_io, ip, tmng_rwr):
        self.__socket_io = socket_io
        self.__ip = ip
        self.__console = console
        self.__tmng_rwr = tmng_rwr
        self.mqtt_thread = Thread()
        self.mqtt_stop = Event()

        self.start()

    def start(self):
        """
        Start
        :return:
        """

        if not self.mqtt_thread.is_alive():
            self.mqtt_thread = MQTT(socket_io=self.__socket_io, ip=self.__ip, console=self.__console,
                                    tmng_rwr=self.__tmng_rwr)
            self.mqtt_thread.start()
