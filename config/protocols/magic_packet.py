from config.protocols.default import Protocol
from wakeonlan import send_magic_packet
from flask_babel import gettext
from threading import Thread

import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import os


class MagicPacketThread(Thread):
    def __init__(self, terminal, general):
        super().__init__()
        self.__terminal = terminal
        self.__general = general

        self.__ips = []
        self.__last_values = []

    def subscribe(self, ip):
        if ip not in self.__ips:
            self.__ips.append(ip)
            self.__last_values.append(None)

    def unsubscribe(self, ip):
        for num, i in enumerate(self.__ips):
            if i == ip:
                self.__ips.pop(num)
                self.__last_values.pop(num)

    @staticmethod
    def ping(host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', host]

        return subprocess.call(command, stdout=open(os.devnull, 'wb')) == 0

    def run(self):
        while True:
            for number, ip in enumerate(self.__ips):
                value = self.ping(ip)
                # if self.__last_values[number] != value:
                self.__last_values[number] = value
                self.__general.update(protocol_type="magic_packet", value=value, config_part={"ip": ip})
            time.sleep(1)


class MagicPacket(Protocol):

    TYPE = "magic_packet"
    VISIBLE = True
    NAME = gettext("Magic Packet")

    SEPARATOR = ":"

    def __init__(self, terminal, update):
        super().__init__(terminal, update)

        if not self.thread.is_alive():
            self.thread = MagicPacketThread(terminal=self._terminal, general=self._general)
            self.thread.start()

    def config(self):
        return {
            self._MAC: ["00" for _ in range(6)],
            self._IP:  "172.16.0.x"
        }

    def edit_config(self):
        from config.items.input import Input

        return {
            self._MAC: Input().make_object(value=self.config()[self._MAC], label=gettext("MAC"), count=6),
            self._IP: Input().make_object(value=self.config()[self._IP], label=gettext("IP"))}

    def publish(self, config, value):
        if value:
            mac = self.SEPARATOR.join(config[self._MAC])
            send_magic_packet(mac)
            self._terminal.protocol("MP", "Waking up {} on {}".format(mac, config[self._IP]))

    def add_listener_inner(self, config):
        self.thread.subscribe(config[self._IP])

    def remove_listener_inner(self, config):
        self.thread.unsubscribe(config[self._IP])
