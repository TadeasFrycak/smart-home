import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

BROKER_IP = "172.16.0.2"
USERNAME = "home"
PASSWORD = "xbYRJocj08YEtazIg90QEYiccembElT1"

DOORBIRD_MQTT = [
    # "rx/doorbird/motionsensor",
    # "tx/doorbird/motionsensor",
    "rx/doorbird/doorbell",
    "tx/doorbird/doorbell",
]

INTRUSION_MQTT = [
    "rx/intrusion/alarm",
    "tx/intrusion/alarm",
]

TEST_MQTT = [
    "rx/piezo/test",
    "tx/piezo/test",
]

PIN = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.LOW)

muted = False


def buzzer(state: int, delay=0.3):
    GPIO.output(PIN, state)
    time.sleep(delay)


def run(self):
    while True:
        if self.__activated.value and not self.__muted.value:
            with self.__activated.get_lock():
                self.__activated.value = False


def on_message(client, userdata, message):
    print(message.topic)
    if message.topic in INTRUSION_MQTT:
        for _ in range(10):
            buzzer(1, 0.5)
            buzzer(0, 0.5)

    elif message.topic in DOORBIRD_MQTT:
        for _ in range(10):
            for _ in range(2):
                buzzer(1, 0.1)
                buzzer(0, 0.1)

            time.sleep(1)

    elif message.topic in TEST_MQTT:
        buzzer(1, 0.1)
        buzzer(0, 0.1)


client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(username=USERNAME, password=PASSWORD)
client.connect(BROKER_IP)

for i in INTRUSION_MQTT + DOORBIRD_MQTT + TEST_MQTT:
    client.subscribe(i)

client.loop_forever()
