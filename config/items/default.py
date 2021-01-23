import random
import string
import time

from library.fmng import FileManager
from flask_babel import gettext


class Item:
    """
    Default item superclass
    """

    TYPE = None
    VISIBLE = False
    NAME = gettext("Unnamed")
    PROTOCOLS = []
    DESCRIPTION = ""
    VALUE = None

    # Arguments
    # TODO na tohle udělat jeden speciální soubor
    _ID = "id"
    _TYPE = "type"
    _VISIBLE = "visible"
    _NAME = "name"
    _DESCRIPTION = "description"
    _VALUE = "value"
    _CONFIG = "config"
    _PROTOCOLS = "protocols"

    # General
    _LABEL = "label"

    # Slider
    _SUFFIX = "suffix"
    _MIN = "min"
    _MAX = "max"
    _STEP = "step"
    _SMOOTH = "smooth"
    _RANGE = "range"
    _DISABLED = "disabled"

    # Toggle
    _PLACEHOLDER = "placeholder"

    # Input
    _NUMBER = "number"
    _READONLY = "readonly"
    _INVALID = "invalid"
    _BUTTON = "button"
    _PREPEND = "prepend"
    _LIST = "list"
    _COUNT = "count"

    # Button
    _COLOR = "color"

    # Button group
    _BUTTONS = "btn_group"
    _CHECKBOX = "checkbox"

    # Dropdown
    _OPTIONS = "options"

    def __init__(self, *args, **kwargs):
        self._fmng = FileManager()
        pass

    @property
    def config(self):
        """
        Method of each item
        Contains all settings of item
        :return: config
        """
        return {}

    @property
    def edit_config(self):
        """
        Method of each item
        Contains all EDITABLE settings of item
        :return: editable item config values
        """
        return {}

    @staticmethod
    def _merge(default, kwargs):
        """
        Merge config with default object
        :param default: default object
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
        Make item object with data to save
        Contains real values
        :param value: value of item
        :param kwargs: kwargs to merge config with default values
        :return: object
        """
        if value is None:
            value = self.VALUE

        return {
            self._ID: self.random_id(),
            self._TYPE: self.TYPE,
            self._VALUE: value,
            self._PROTOCOLS: [],
            self._VISIBLE: True,  # TODO this is for implement in future (hide function in edit)
            self._CONFIG: self._merge(default=self.config, kwargs=kwargs)
        }

    def make_full_object(self):
        """
        Make full object of current item for edit mode
        Contains all recursive objects in one
        Only "layout" - items to set values
        :return: object
        """
        return {
            self._ID: self.random_id(),
            self._TYPE: self.TYPE,
            self._VISIBLE: self.VISIBLE,
            self._NAME: self.NAME,
            self._DESCRIPTION: self.DESCRIPTION,
            self._VALUE: self.VALUE,
            self._PROTOCOLS: [],
            self._CONFIG: self.edit_config
        }
