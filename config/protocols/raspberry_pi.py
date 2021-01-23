from config.protocols.default import Protocol
from flask_babel import gettext
import gpiozero


class RaspberryPi(Protocol):
    TYPE = "raspberry_pi"
    VISIBLE = True
    NAME = gettext("RPi")

    def config(self):
        return {
            self._PIN: "00:00:00:00:00:00",
            self._BCM: True
        }

    def edit_config(self):
        from config.items.toggle import Toggle
        from config.items.input import Input

        return {
            self._PIN: Input().make_object(value=self.config()[self._PIN], label=gettext("Pin")),
            self._BCM: Toggle().make_object(value=self.config()[self._BCM], label=gettext("BCM"))}
