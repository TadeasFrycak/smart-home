from threading import Thread, Event
import paho.mqtt.client as mqtt
import time


class ArduinoAcom(Thread):
    """
    Arduino asynchronous communication class
    """

    DELAY = 0.1

    def __init__(self, socket_io, arduino, arduino_stop):
        """
        Init of Arduino asynchronous communication class
        :param socket_io: declare of socket_io
        :param arduino: declare of arduino
        :param arduino_stop: declare of arduino_stop
        """

        super(ArduinoAcom, self).__init__()
        self.__socket_io = socket_io
        self.__arduino = arduino
        self.__arduino_stop = arduino_stop

    def arduino(self):
        """
        Data class
        :return:
        """

        raw_data = self.__arduino.read()

        if raw_data is not None:
            data = json.loads(html_json.to_json(raw_data))

            if "alarm" in data.keys():
                # subprocess.check_output(["omxplayer", "alarm.mp3"]).decode("utf-8")
                socket_io.emit("notify", {"title": "Poplach", "message": "Senzor - postel", "type": "info"},
                               namespace="/acom")

    def run(self):
        """
        Run thread
        :return:
        """

        while not self.__arduino_stop.isSet():
            self.arduino()
            time.sleep(self.DELAY)


class RaspberryAcom(Thread):
    """
    Raspberry asynchronous communication class
    """

    DELAY = 300
    NAMESPACE = "/acom"

    def __init__(self, socket_io, raspberry_stop):
        """
        Init of Raspberry asynchronous communication class
        :param socket_io: socket_io
        :param raspberry_stop: raspberry_stop
        """

        super(RaspberryAcom, self).__init__()
        self.__raspberry_stop = raspberry_stop
        self.__socket_io = socket_io

    def cpu_temp(self):
        """
        Measure CPU temp, append to Raspberry item (graph)
        :return:
        """

        data_x = str(datetime.datetime.now().strftime("%H:%M"))
        data_y = raspberry.cpu_temp()
        element_id = "modal-graph-1"
        id_tile = "raspberry-1"

        tmng.graph_rwr(id_tile=id_tile, data_x=data_x, data_y=data_y, element_id=element_id)
        self.__socket_io.emit("graphs", {tmng.DATA_Y: data_y, tmng.DATA_X: data_x, tmng.ID: element_id,
                                         tmng.TILE_ID: id_tile}, namespace=self.NAMESPACE)

    def test_graph(self):
        """
        Test graph
        :return:
        """

        data_x = str(datetime.datetime.now().strftime("%H:%M"))
        data_y = random.randint(0, 100)
        element_id = "modal-graph-1"
        id_tile = "raspberry-1"

        tmng.graph_rwr(id_tile=id_tile, data_x=data_x, data_y=data_y, element_id=element_id)
        self.__socket_io.emit("graphs", {tmng.DATA_Y: data_y, tmng.DATA_X: data_x, tmng.ID: element_id,
                                         tmng.TILE_ID: id_tile}, namespace=self.NAMESPACE)

    def run(self):
        """
        Run thread
        :return:
        """

        while not self.__raspberry_stop.isSet():
            # self.cpu_temp()
            time.sleep(self.DELAY)


class MQTT(Thread):
    """
    MQTT class
    """

    NAMESPACE = "acom"  # TODO sjednotit
    BROKER = "192.168.0.100"
    PORT = 1883
    USER = "username"
    PASSWORD = "12345678"
    HOME = "home"

    def __init__(self, console, arduino, socket_io):
        """
        Init of MQTT class
        :param console: Console class
        :param arduino: Arduino class
        :param socket_io: declare of socket_io
        """

        super(MQTT, self).__init__()

        self.__client = None
        self.__console = console
        self.__socket_io = socket_io
        self.__arduino = arduino

    def on_connect(self, client, userdata, flags, rc):
        """
        On connect
        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return:
        """

        # print("Connected with result code " + str(rc))
        self.client.subscribe(HOME + "/#")

    def on_message(self, client, userdata, msg):
        """
        On message
        :param client:
        :param userdata:
        :param msg:
        :return:
        """

        topic = msg.topic
        id_tile = topic.split("/")[1]

        try:
            element_id = topic.split("/")[2]

        except Exception as e:
            self.__socket_io.emit("tile", {tmng.ID: id_tile, tmng.VALUE: msg.payload.decode()},
                                  namespace=self.NAMESPACE)

        else:
            self.__arduino.write(
                html_json.to_html(json_data={tmng.ID: "bed-toggle", tmng.TILE_ID: "bed-toggle",
                                             tmng.VALUE: msg.payload.decode()}))

            self.__socket_io.emit("slider", {tmng.TILE_ID: id_tile, tmng.ID: element_id,
                                             tmng.VALUE: msg.payload.decode()}, namespace=self.NAMESPACE)

            self.__socket_io.emit("toggle", {tmng.TILE_ID: id_tile, tmng.ID: element_id,
                                             tmng.VALUE: msg.payload.decode()}, namespace=self.NAMESPACE)

        # self.client.disconnect()

    def run(self):
        """
        Run thread
        :return:
        """

        self.__client = mqtt.Client()

        try:
            self.__client.connect(self.BROKER, self.PORT, 60)

        except Exception as e:
            self.__console.print("MQTT is not working. Some functions may not work.", priority=2)

        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message
        self.__client.loop_forever()


class Acom:
    """
    Asynchronous communication class
    """

    def __init__(self, console, arduino, socket_io):
        """
        Init of asynchronous communication class
        :param console: Console class
        :param arduino: Arduino class
        :param socket_io: declare of socket_io
        """

        self.__console = console
        self.__arduino = arduino
        self.__socket_io = socket_io

        self.mqtt_thread = Thread()
        self.mqtt_stop = Event()

        self.raspberry_thread = Thread()
        self.raspberry_stop = Event()

        self.arduino_thread = Thread()
        self.arduino_stop = Event()

        self.start()

    def start(self):
        """
        Start
        :return:
        """

        if not self.raspberry_thread.is_alive():
            self.raspberry_thread = RaspberryAcom(socket_io=self.__socket_io, raspberry_stop=self.raspberry_stop)
            self.raspberry_thread.start()

        if not self.arduino_thread.is_alive():
            self.arduino_thread = ArduinoAcom(socket_io=self.__socket_io, arduino_stop=self.arduino_stop,
                                              arduino=self.__arduino)
            self.arduino_thread.start()

        if not self.mqtt_thread.is_alive():
            self.mqtt_thread = MQTT(console=self.__console, arduino=self.__arduino, socket_io=self.__socket_io)
            self.mqtt_thread.start()
