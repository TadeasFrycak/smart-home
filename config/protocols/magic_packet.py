from config.protocols.default import Protocol
from wakeonlan import send_magic_packet
from flask_babel import gettext


class MagicPacket(Protocol):

    TYPE = "magic_packet"
    VISIBLE = True
    NAME = gettext("Magic Packet")

    __HOME = "home"

    def config(self):
        return {
            self._MAC: "00:00:00:00:00:00",
            self._IP:  "192.168.88.xx"
        }

    def edit_config(self):
        from config.items.input import Input

        return {
            self._MAC: Input().make_object(value=self.config()[self._MAC], label=gettext("MAC")),
            self._IP: Input().make_object(value=self.config()[self._IP], label=gettext("IP"))}

    def publish(self, config, value):
        send_magic_packet(config[self._MAC])
