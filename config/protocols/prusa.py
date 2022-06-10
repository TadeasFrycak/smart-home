from config.protocols.default import Protocol
from flask_babel import gettext
from threading import Thread
import serial
import time


class PrusaThread(Thread):
    def __init__(self, terminal, general):
        super().__init__()
        self.__terminal = terminal
        self.__general = general

        # TODO autovýběr portu podle jména (je tam napsáno Original Prusa)
        self.arduino = None

        self.status = None
        self.connected = None

    def subscribe(self, ip):
        pass

    def unsubscribe(self, ip):
        pass

    # Read & write
    def read(self, all_lines=True):
        msg = []
        while self.arduino.in_waiting:
            data = self.arduino.readline().decode("utf-8").strip()
            msg.append(data)

            if not all_lines:
                break

        return ";".join(msg)

    def write(self, msg):
        self.arduino.write(bytes("{}\n".format(msg), encoding="utf8"))

    def write_cmd(self, command, value="", argument=""):
        self.write(f"{command} {argument}{value}")

        time.sleep(0.2)

        return self.read()

    # Commands
    def display_text(self, text):
        if len(text) <= 20:
            return self.write_cmd("M117", text) == "ok"

    def heat_bed(self, temperature):
        if 0 <= temperature <= 100:
            return self.write_cmd("M140", temperature, "S") == "ok"

    def heat_nozzle(self, temperature):
        if 0 <= temperature <= 100:
            return self.write_cmd("M104", temperature, "S") == "ok"

    def cool_down(self):
        self.heat_bed(0)
        self.heat_nozzle(0)

    def home(self):
        return self.write_cmd("G28", "W") == "ok"

    def connect(self):
        while True:
            print("Connecting.....")
            try:
                self.arduino = serial.Serial("/dev/ttyACM0", 115200, timeout=3)
                self.init()
                break

            except serial.serialutil.SerialException:
                try:
                    self.arduino = serial.Serial("/dev/ttyACM1", 115200, timeout=3)
                    self.init()
                    break

                except serial.serialutil.SerialException:
                    self.status = "offline"
                    time.sleep(5)

    def init(self):
        print("Connected!")
        self.status = "online"
        self.connected = time.time()

        time.sleep(10)

        self.display_text("  Connected to SH!  ")

        pass

    def measure(self):
        print(self.read(True))
        if time.time() - self.connected > 10:
            print("Buzzer", self.write_cmd("M300 S440 P100"))

    def run(self):
        self.connect()

        # print("Ping", self.write_cmd("PRUSA", "Ping"))
        # print("PRN", self.write_cmd("PRUSA", "PRN"))
        # print("FAN", self.write_cmd("PRUSA", "FAN"))
        # print("Fir", self.write_cmd("PRUSA", "Fir"))
        # print("Rev", self.write_cmd("PRUSA", "Rev"))
        # print("temperature interpolation", self.write_cmd("G75"))
        # print("SD status", self.write_cmd("M27"))

        # TODO G92 - pozicování
        # TODO M17
        # TODO M28, M29, M30 - gcode live
        # TODO M31 time

        # TODO M112 stop
        # TODO M105 teploty
        # TODO M106 fan speed
        # TODO M84, M18 - disable steppers
        # TODO M85 - shutdown
        # TODO M86 - cool down after time
        # TODO M115 firmware info
        # TODO M114 current position
        # TODO M300 play tone
        # TODO M503 - all settings in memory
        # TODO M600, M701, M702 - load, unload filament
        # TODO M862

        # Při tisku:
        # TODO M73 print progress
        # TODO M601, M25 - pause print
        # TODO M602 - resume print
        # TODO M603 - stop print
        while True:
            try:
                print("Measuring...")
                self.measure()
                time.sleep(5)

            except OSError:
                print("Disconnected")
                self.connect()


class Prusa(Protocol):

    TYPE = "prusa"
    VISIBLE = True
    NAME = gettext("Prusa")

    SEPARATOR = ":"

    def __init__(self, terminal, update):
        super().__init__(terminal, update)

        if not self.thread.is_alive():
            self.thread = PrusaThread(terminal=self._terminal, general=self._general)
            self.thread.start()

    def config(self):
        return {
            self._COMMAND: "",
            self._ARGUMENT: "",
            self._READ_ALL: False,
            self._SEND_VALUE: True
        }

    def edit_config(self):
        from config.items.input import Input
        from config.items.toggle import Toggle

        return {
            self._COMMAND: Input().make_object(value=self.config()[self._COMMAND], label=gettext("Command")),
            self._ARGUMENT: Input().make_object(value=self.config()[self._ARGUMENT], label=gettext("Argument")),
            self._READ_ALL: Toggle().make_object(value=self.config()[self._READ_ALL], label=gettext("Read tile states")),
            self._SEND_VALUE: Toggle().make_object(value=self.config()[self._READ_ALL], label=gettext("Send my value"))
        }

    def publish(self, config, value):
        self._terminal.protocol("PRUSA", "Sending command '{}' with argument '{}' and value '{}'".format(config[self._COMMAND], config[self._ARGUMENT], value))
        if config[self._SEND_VALUE]:
            self.thread.write_cmd(config[self._COMMAND], value, config[self._ARGUMENT])
        else:
            self.thread.write_cmd(config[self._COMMAND])
