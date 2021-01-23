from flask_babel import gettext
from config.tiles.default import Tile


class Player(Tile):
    """
    Player tile subclass
    """

    TYPE = "player"
    VISIBLE = False
    NAME = gettext("Player")
