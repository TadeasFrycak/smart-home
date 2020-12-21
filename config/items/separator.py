from flask_babel import lazy_gettext
from config.items.default import Item


class Separator(Item):
    """
    Separator item subclass
    """

    TYPE = "separator"
    VISIBLE = True
    NAME = lazy_gettext("Separator")
    DESCRIPTION = lazy_gettext("Separate content")
