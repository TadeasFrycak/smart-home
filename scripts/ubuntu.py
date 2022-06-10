# sudo apt install gnome-screensaver

from threading import Thread, Event
import paho.mqtt.client as mqtt
import subprocess
import time

# TODO SH - ovládání PC - udělat skritp, který se připojí na MQTT a bude interagovat:
# - Zhasnout monitory
# - uspat
# - vypnout
# - restartovat
# - výchozí audio výstup - https://askubuntu.com/questions/1038490/how-do-you-set-a-default-audio-output-device-in-ubuntu-18-04
# - ...

BROKER_IP = "home.cz"
USERNAME = "home"
PASSWORD = "xbYRJocj08YEtazIg90QEYiccembElT1"

HOME_SEND = "tx/pokojicek/stolni_pc/"
HOME_RECEIVE = "rx/pokojicek/stolni_pc/"

volume_updated = 0


def on_message(client, userdata, message):
    global volume_updated
    if message.topic == HOME_SEND + "lock":
        subprocess.check_output(["gnome-screensaver-command", "-l"])

    elif message.topic == HOME_SEND + "volume":
        volume_updated = time.time()
        subprocess.check_output(["amixer", "-D", "pulse", "sset", "Master", "{}%".format(message.payload.decode("utf-8"))])
    
    elif message.topic == HOME_SEND + "pause":
        subprocess.check_output(["pacmd", "suspend", message.payload.decode("utf-8")])


client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(username=USERNAME, password=PASSWORD)
client.connect(BROKER_IP)
client.subscribe(HOME_SEND + "lock")
client.subscribe(HOME_SEND + "volume")
client.subscribe(HOME_SEND + "pause")


class Measuring(Thread):
    def __init__(self):
        super().__init__()
        
        self.volume_last_value = None
        self.uptime_last_value = None

    def run(self):
        while True:
            # Uptime
            data_uptime = subprocess.check_output(["awk", """
            {print int($1/86400)"d "int($1%86400/3600)"h "int(($1%3600)/60)"min"}
            """, "/proc/uptime"])  # "int($1%60)"s
            
            if data_uptime != self.uptime_last_value:
                client.publish(HOME_RECEIVE + "uptime", data_uptime)
                self.uptime_last_value = data_uptime

            # Volume    
            if time.time() - volume_updated > 3:
                volume = subprocess.check_output(["amixer", "-D", "pulse", "sget", "Master"]).decode("utf-8")
                channel = volume.split("Playback channels:")[1].split("\n")[0].strip().split(" - ")[0] + ":"
                data_volume = volume.split(channel)[1].split("\n")[0].strip().split("[")[1].split("]")[0].rstrip("%")
                
                
                if data_volume != self.volume_last_value:
                    client.publish(HOME_RECEIVE + "volume", data_volume)
                    self.volume_last_value = data_volume


            time.sleep(1)


measuring_thread = Thread()
measuring_stop = Event()

if not measuring_thread.is_alive():
    measuring_thread = Measuring()
    measuring_thread.start()

client.loop_forever()
