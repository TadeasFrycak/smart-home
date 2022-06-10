from flask_babel import gettext
from config.items.default import Item


class Separator(Item):
    """
    Separator item subclass
    """

    TYPE = "separator"
    VISIBLE = True
    NAME = gettext("Separator")
