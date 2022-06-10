import json
from threading import Thread, Event
import paho.mqtt.client as mqtt
import subprocess
import time
import datetime

BROKER_IP = "172.16.0.2"
USERNAME = "home"
PASSWORD = "xbYRJocj08YEtazIg90QEYiccembElT1"

HOME_SEND = "tx"
HOME_RECEIVE = "rx/ups/"


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(username=USERNAME, password=PASSWORD)
client.connect(BROKER_IP)


class Measuring(Thread):
    def __init__(self):
        super().__init__()

        self.time_backup = 0

    @staticmethod
    def export(data):
        data = data.strip().split("\n")

        final_dict = dict()

        for i in data:
            split_data = i.split(": ")

            header = split_data[0]
            value = split_data[1]

            final_dict[header] = value

        return final_dict

    @staticmethod
    def percentage(value, suffix):
        return json.dumps({"value": value, "suffix": suffix})

    def run(self):
        while True:
            data = self.export(subprocess.check_output(["sudo", "upsc", "cyberpower1@localhost"], stderr=None).decode("utf-8"))
            battery_capacity = data["battery.charge"]
            battery_voltage = data["battery.voltage"]
            battery_runtime = str(int(data["battery.runtime"]) / 100)

            input_voltage = data["input.voltage"]
            output_voltage = data["output.voltage"]

            ups_model = data["ups.model"]
            ups_status = data["ups.status"]
            ups_load = data["ups.load"]

            if ups_status == "OL":
                ups_status = "Ok"
                self.time_backup = 0

            elif ups_status == "OB DISCHRG":
                if not self.time_backup:
                    self.time_backup = datetime.datetime.fromtimestamp(time.time())

                time_blackout = self.time_backup.strftime("%H:%M")
                ups_status = f"Výpadek sítě od {time_blackout}, záloha z baterií"

            client.publish(HOME_RECEIVE + "battery/charge/tile", self.percentage(battery_capacity, "%"))
            client.publish(HOME_RECEIVE + "battery/voltage/tile", self.percentage(battery_voltage, "V"))
            client.publish(HOME_RECEIVE + "battery/runtime/tile", self.percentage(battery_runtime, "min"))

            client.publish(HOME_RECEIVE + "battery/charge", battery_capacity + " %")
            client.publish(HOME_RECEIVE + "battery/voltage", battery_voltage + " V")
            client.publish(HOME_RECEIVE + "battery/runtime", battery_runtime + " min")

            client.publish(HOME_RECEIVE + "input/voltage/tile", self.percentage(input_voltage, "V"))
            client.publish(HOME_RECEIVE + "output/voltage/tile", self.percentage(output_voltage, "V"))

            client.publish(HOME_RECEIVE + "input/voltage", input_voltage + " V")
            client.publish(HOME_RECEIVE + "output/voltage", output_voltage + " V")

            client.publish(HOME_RECEIVE + "model", ups_model)
            client.publish(HOME_RECEIVE + "status", ups_status)

            client.publish(HOME_RECEIVE + "load/tile", self.percentage(ups_load, "W"))
            client.publish(HOME_RECEIVE + "load", ups_load + " W")

            time.sleep(30)


measuring_thread = Thread()
measuring_stop = Event()

if not measuring_thread.is_alive():
    measuring_thread = Measuring()
    measuring_thread.start()

client.loop_forever()
# client.loop_stop()
