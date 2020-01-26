import RPi.GPIO as GPIO
import subprocess


class Raspberry:
    """
    Raspberry Pi class
    """

    FAN_PIN = 14

    def __init__(self):
        """
        Init of Raspberry Pi class
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.FAN_PIN, GPIO.OUT)

    @staticmethod
    def cpu_temp():
        """
        Measure CPU temp
        :return:
        """

        temp = int(subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]).decode("utf-8").strip().split("=")[
                       1].split(".")[0])
        return temp

    def set_fan(self, state):
        """
        Turn on/off CPU fan
        :param state:
        :return:
        """

        GPIO.output(self.FAN_PIN, state)  # TODO PWM
