import random
import string
import time

from flask_babel import gettext


class Tile:
    """
    Default tile superclass
    """

    TYPE = None
    VISIBLE = False
    NAME = gettext("Unnamed")
    PROTOCOLS_ABLE = []
    PROTOCOLS = []

    LABEL = gettext("Unnamed")
    VALUE = None

    # Arguments
    # TODO na tohle udělat jeden speciální soubor
    _ID = "id"
    _TYPE = "type"
    _MODAL = "modal"
    _LABEL = "label"
    _VISIBLE = "visible"
    _NAME = "name"
    _VALUE = "value"
    _CONFIG = "config"
    _PROTOCOLS = "protocols"
    _PROTOCOLS_ABLE = "protocols_able"

    _ICON = "icon"

    def __init__(self, *args, **kwargs):
        pass

    @property
    def config(self):
        """
        Method of each tile
        Contains all settings of tile
        :return: config
        """
        return {}

    @property
    def edit_config(self):
        """
        Method of each tile
        Contains all EDITABLE settings of tile
        :return: editable item config values
        """
        return {}

    @staticmethod
    def _merge(default, kwargs):
        """
        Merge config with default object
        :param default: default objecton_display_value
        :param kwargs: config
        :return: merged object
        """
        for kwarg in kwargs:
            default[kwarg] = kwargs[kwarg]

        return default

    @staticmethod
    def on_new_value(before, current):
        return current

    @staticmethod
    def on_display_value(value):
        return value

    @staticmethod
    def create_random_string(length=2):
        return "".join(random.choices(string.ascii_lowercase, k=length))

    def random_id(self):
        """
        Make random ID
        :return: random ID
        """
        random_id = self.create_random_string() + "-" + str(time.time())

        return random_id

    def make_object(self, value=None, **kwargs):
        """
        Make tile object with data to save
        Contains real values
        :param value: value of tile
        :param kwargs: kwargs to merge config with default values
        :return: object
        """
        if value is None:
            value = self.VALUE

        return {
            self._ID: self.random_id(),
            self._TYPE: self.TYPE,
            self._MODAL: [],
            self._VALUE: value,
            self._PROTOCOLS: self.PROTOCOLS,
            self._VISIBLE: True,  # TODO this is for implement in future
            self._CONFIG: self._merge(default=self.config, kwargs=kwargs)
        }

    def make_full_object(self):
        """
        Make full object of current tile for edit mode
        Contains all recursive objects in one
        Only "layout" - items to set values
        :return: object
        """
        return {
            self._ID: self.random_id(),
            self._MODAL: [],
            self._TYPE: self.TYPE,
            self._VISIBLE: self.VISIBLE,
            self._NAME: self.NAME,
            self._LABEL: self.LABEL,
            self._VALUE: self.VALUE,
            self._PROTOCOLS: self.PROTOCOLS,
            self._PROTOCOLS_ABLE: self.PROTOCOLS_ABLE,
            self._CONFIG: self.edit_config
        }
