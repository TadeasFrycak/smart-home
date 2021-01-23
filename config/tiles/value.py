from flask_babel import gettext
from config.tiles.default import Tile


class Value(Tile):
    """
    Value tile subclass
    """

    TYPE = "value"
    VISIBLE = True
    NAME = gettext("Value")
    VALUE = {"value": "Null", "time": None, "suffix": ""}
