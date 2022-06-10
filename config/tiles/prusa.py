from flask_babel import gettext
from config.tiles.default import Tile


class Prusa(Tile):
    """
    Prusa tile subclass
    """

    TYPE = "prusa"
    VISIBLE = True
    NAME = gettext("Prusa")
    PROTOCOLS_ABLE = ["mqtt"]
    VALUE = {
        "percentage": 0,
        "time": "0d 0h 0min",
        "status": gettext("Not running"),
        "hotend": 0,
        "bed": 0
    }
