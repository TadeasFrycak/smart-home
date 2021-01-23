from flask_babel import gettext
from config.tiles.default import Tile


class Blank(Tile):
    """
    Blank tile subclass
    """

    TYPE = "blank"
    VISIBLE = True
    NAME = gettext("Blank")
    VALUE = False
