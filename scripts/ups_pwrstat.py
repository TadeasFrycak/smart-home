import json
from threading import Thread, Event
import paho.mqtt.client as mqtt
import subprocess
import time

BROKER_IP = "127.0.1.1"
USERNAME = "home"
PASSWORD = "xbYRJocj08YEtazIg90QEYiccembElT1"

HOME_SEND = "client"
HOME_RECEIVE = "home/"


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(username=USERNAME, password=PASSWORD)
client.connect(BROKER_IP)


class Measuring(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            data = subprocess.check_output(["sudo", "pwrstat", "-status"])
            battery_capacity = int(str(data).split("Battery Capacity............. ")[1].split(" %")[0])
            input_voltage = int(str(data).split("Utility Voltage.............. ")[1].split(" V")[0])
            output_voltage = int(str(data).split("Output Voltage............... ")[1].split(" V")[0])
            remaining_runtime = int(str(data).split("Remaining Runtime............ ")[1].split(" min.")[0])
            load = int(str(data).split("Load......................... ")[1].split(" Watt")[0])

            client.publish(HOME_RECEIVE + "battery-capacity", json.dumps({"value": battery_capacity, "suffix": "%"}))
            client.publish(HOME_RECEIVE + "input-voltage", json.dumps({"value": input_voltage, "suffix": "V"}))
            client.publish(HOME_RECEIVE + "output-voltage", json.dumps({"value": output_voltage, "suffix": "V"}))
            client.publish(HOME_RECEIVE + "remaining-runtime", json.dumps({"value": remaining_runtime, "suffix": "min"}))
            client.publish(HOME_RECEIVE + "ups-load", json.dumps({"value": load, "suffix": "W"}))

            time.sleep(3)


measuring_thread = Thread()
measuring_stop = Event()

if not measuring_thread.is_alive():
    measuring_thread = Measuring()
    measuring_thread.start()

client.loop_forever()
# client.loop_stop()


