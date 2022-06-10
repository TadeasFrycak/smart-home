from threading import Thread, Event
import paho.mqtt.client as mqtt
import serial
import time
import json


BROKER_IP = "127.0.0.1"
USERNAME = "home"
PASSWORD = "xbYRJocj08YEtazIg90QEYiccembElT1"

HOME_SEND = "tx/serverovna/prusa/"
HOME_RECEIVE = "rx/serverovna/prusa/"


class PrusaThread(Thread):
    CONNECTED_NOT_PRINTING = "Connected, not printing"
    CONNECTED_SD_EJECTED = "Connected, SD ejected!"
    CONNECTED_DONE_PRINTING = "Connected, done printing!"
    CONNECTED_WAITING = "Connected, waiting for user..."
    CONNECTED_HEATING = "Heating before printing..."
    CONNECTED_INITIALISING = "Connected, initialising"

    CONNECTED_POWER_OFF = "Connected, power off!"

    DISCONNECTED = "Disconnected!"

    def __init__(self, client):
        super().__init__()
        self.__client = client

        # TODO autovýběr portu podle jména (je tam napsáno Original Prusa)
        self.arduino = None

        self.status = None
        self.nozzle = 0
        self.bed = 0
        self.percentage = 0
        self.time = "0h 0m"

        self.sd = None
        self.power_off = None

        self.connected = None

    def update_tile(self):
        if self.status == self.CONNECTED_NOT_PRINTING and self.sd is False:
            self.status = self.CONNECTED_SD_EJECTED

        data = {
            "status": self.status,
            "time": self.time,
            "percentage": self.percentage,
            "hotend": self.nozzle,
            "bed": self.bed,
        }
        self.__client.publish(HOME_RECEIVE + "main", json.dumps(data))

    # Read & write
    def process_data(self, data):
        not_my = []
        for i in data:
            print(i)
            if "T:" in i and "B:" in i:
                if not ("P:" in i and "A:" in i) and "E:" in i:
                    self.status = self.CONNECTED_HEATING

                self.nozzle = round(float(i.split("T:")[1].split()[0]))
                self.bed = round(float(i.split("B:")[1].split()[0]))

                self.update_tile()

            elif "echo:busy: paused for user" in i:
                self.status = self.CONNECTED_WAITING
                self.update_tile()

            elif "echo:SD init fail" in i:
                self.sd = False
                self.status = self.CONNECTED_SD_EJECTED
                self.update_tile()

            elif "echo:SD card ok" in i:
                self.sd = True
                self.status = self.CONNECTED_NOT_PRINTING
                self.update_tile()

            elif "Not SD printing" in i:
                self.status = self.CONNECTED_NOT_PRINTING

            elif "Done printing file" in i:
                self.status = self.CONNECTED_DONE_PRINTING
                self.update_tile()

            elif "NORMAL MODE: Percent done:" in i and "print time remaining in mins: " in i:
                self.percentage = int(i.split("Percent done: ")[1].split(";")[0])

                time_minutes = int(i.split("print time remaining in mins: ")[1].strip())
                days = time_minutes // 1_440
                time_minutes = time_minutes % 1_440
                hours = time_minutes // 60
                time_minutes = time_minutes % 60
                minutes = time_minutes

                if days > 0:
                    self.time = f"{days}d {hours}h {minutes}m"

                else:
                    self.time = f"{hours}h {minutes}m"

                self.update_tile()

            elif "INT4" in i:
                self.status = self.CONNECTED_POWER_OFF
                self.power_off = True
                self.update_tile()

            elif ".gco" in i and "File opened:" not in i and "echo:" not in i:
                self.status = i
                self.update_tile()

            else:
                not_my.append(i)

        if len(not_my) > 1:
            if "ok" in not_my:
                not_my.remove("ok")

        return not_my

    def read(self, all_lines=True):
        try:
            msg = []
            while self.arduino.in_waiting:
                data = self.arduino.readline().decode("utf-8").strip()
                msg.append(data)

                if not all_lines:
                    break

            return ";".join(self.process_data(msg))

        except OSError:
            self.connect()

    def write(self, msg, wait=False):
        try:
            self.read()
            self.arduino.write(bytes("{}\n".format(msg), encoding="utf8"))
            if wait:
                time.sleep(0.3)
                return self.read()

        except OSError:
            self.connect()

    # Commands
    def display_text(self, text):
        if len(text) <= 20:
            self.write(f"M117 {text}")

    def heat_bed(self, temperature):
        if 0 <= temperature <= 100:
            self.write(f"M140 S{temperature}")

    def heat_nozzle(self, temperature):
        if 0 <= temperature <= 100:
            self.write(f"M104 S{temperature}")

    def cool_down(self):
        self.heat_bed(0)
        self.heat_nozzle(0)

    def buzzer(self, frequency=440, delay=100):
        if 50 <= frequency <= 20_000:
            if 1 <= delay <= 1_000:
                self.write(f"M300 S{frequency} P{delay}")

    def fan(self, speed):
        if 0 <= speed <= 255:
            self.write(f"M106 S{speed}")  # M107 - turn fan off

    def home(self):
        self.write("G28 W")

    def temperatures(self):
        self.write("M105")

    def print_progress(self):
        self.write("M73")

    def sd_status(self):
        self.write("M27")

    # Filament
    def load_filament(self):
        self.write("M701")  # M600 - pause for filament change

    def unload_filament(self):
        self.write("M702")

    # SD card
    def initialize_sd(self):
        self.write("M21")

    def release_sd(self):
        self.write("M22")

    # Pause, stop, emergency stop
    # TODO M601, M25 - pause printing
    # TODO M602 - resume printing
    # TODO M603, M0, M1 - stop printing
    # TODO M112 - emergency stop

    # Other
    # TODO M17, M18, M84 - disable and enable stepper motors
    # TODO (M862)
    # TODO (G75) - Temperature interpolation

    def connect(self):
        while True:
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
                    self.status = self.DISCONNECTED
                    self.update_tile()
                    time.sleep(5)

    def init(self, skip_init=False):
        time.sleep(4)
        self.connected = time.time()
        self.sd = None

        total_time = 10
        dots = 10

        if not skip_init:
            for i in range(dots):
                self.status = self.CONNECTED_INITIALISING + "."*i
                self.update_tile()
                time.sleep(total_time/dots)

        while True:
            if self.write("PRUSA Ping", True) == "ok":
                self.power_off = False

                if skip_init:
                    for i in range(dots):
                        self.status = self.CONNECTED_INITIALISING + "." * i
                        self.update_tile()
                        time.sleep(total_time / dots)

                self.status = self.CONNECTED_NOT_PRINTING
                self.update_tile()

                self.display_text("  Connected to SH!  ")
                break

            else:
                self.power_off = True
                self.status = self.CONNECTED_POWER_OFF
                self.update_tile()

            time.sleep(3)

    def run(self):
        self.connect()

        self.__client.publish(HOME_RECEIVE + "firmware", self.write("PRUSA Fir", True))
        self.__client.publish(HOME_RECEIVE + "revision", self.write("PRUSA Rev", True))

        # print("M115", self.write("M115", True))  # Firmware info

        # TODO G92 - pozicování
        # TODO M114 current position

        # TODO M28, M29, M30 - gcode live
        # TODO M31 time

        # TODO M503 - all settings in memory

        self.sd_status()

        temp_ask = 0
        sd_ask = 0

        while True:
            if self.power_off:
                self.init(True)

            if ((temp_ask >= 30 and ".gco" in self.status) or (temp_ask >= 3 and ".gco" not in self.status)) and self.status != self.CONNECTED_HEATING:
                self.temperatures()
                temp_ask = 0

            if (sd_ask >= 200 and ".gco" in self.status) or (sd_ask >= 5 and ".gco" not in self.status):
                if self.status == self.CONNECTED_DONE_PRINTING:
                    if sd_ask >= 500:
                        self.sd_status()
                        sd_ask = 0
                else:
                    self.sd_status()
                    sd_ask = 0

            temp_ask += 1
            sd_ask += 1

            time.sleep(10)
            self.read()


measuring_thread = Thread()
measuring_stop = Event()


def on_message(client, userdata, message):
    if message.topic == HOME_SEND + "buzzer":
        measuring_thread.buzzer()

    if message.topic == HOME_SEND + "cool_down":
        client.publish(HOME_RECEIVE + "bed", 0)
        client.publish(HOME_RECEIVE + "nozzle", 0)
        measuring_thread.cool_down()

    elif message.topic == HOME_SEND + "bed":
        measuring_thread.heat_bed(int(message.payload.decode("utf-8")))

    elif message.topic == HOME_SEND + "nozzle":
        measuring_thread.heat_nozzle(int(message.payload.decode("utf-8")))

    elif message.topic == HOME_SEND + "fan":
        measuring_thread.fan(int(message.payload.decode("utf-8")) * 2.55)

    elif message.topic == HOME_SEND + "home":
        measuring_thread.home()


client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(username=USERNAME, password=PASSWORD)
client.connect(BROKER_IP)
client.subscribe(HOME_SEND + "buzzer")
client.subscribe(HOME_SEND + "cool_down")
client.subscribe(HOME_SEND + "bed")
client.subscribe(HOME_SEND + "nozzle")
client.subscribe(HOME_SEND + "fan")

if not measuring_thread.is_alive():
    measuring_thread = PrusaThread(client)
    measuring_thread.start()

client.loop_forever()
