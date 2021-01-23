from threading import Thread, Event
from flask_babel import gettext


class Protocol:
    TYPE = None
    VISIBLE = False
    NAME = gettext("Unnamed")

    _TYPE = "type"
    _VISIBLE = "visible"
    _NAME = "name"
    _CONFIG = "config"

    # Mqtt
    _PATH = "path"

    # Magic packet
    _MAC = "mac"
    _IP = "ip"

    # Raspberry Pi
    _PIN = "pin"
    _BCM = "bcm"

    # Timer
    _TIME = "time"

    def __init__(self, terminal, general):
        self._terminal = terminal
        self._general = general

        self.thread = Thread()  # TODO někde může být dynamicky více threadů - třeba magic packet - ping
        self.thread_stop = Event()

    def config(self):
        raise NotImplementedError

    def edit_config(self):
        raise NotImplementedError

    # Protocol publish
    def publish(self, config, value):
        pass

    # Protocol listener
    def add_listener(self, config=None):
        if config:
            final_config = config
        else:
            final_config = self.make_object()[self._CONFIG]

        if self._general.get_count(self.TYPE, final_config) == 1:
            self.add_listener_inner(final_config)

    def add_listener_inner(self, config):
        pass

    def remove_listener_inner(self, config):
        pass

    def remove_listener(self, config):
        if self._general.get_count(self.TYPE, config) == 0:
            self.remove_listener_inner(config)

    def edit_listener(self, old_config, new_config):
        self.remove_listener(old_config)
        self.add_listener(new_config)

    @staticmethod  # TODO tohle dát do speciálního souboru, i v tiles, i v items
    def _merge(default, kwargs):
        for kwarg in kwargs:
            default[kwarg] = kwargs[kwarg]

        return default

    def make_object(self, **kwargs):
        return {
            self._TYPE: self.TYPE,
            self._CONFIG: self._merge(default=self.config(), kwargs=kwargs)
        }

    def make_full_object(self):
        return {
            self._TYPE: self.TYPE,
            self._VISIBLE: self.VISIBLE,
            self._NAME: self.NAME,
            self._CONFIG: self.edit_config()
        }
