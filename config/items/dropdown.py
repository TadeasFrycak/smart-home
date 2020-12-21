from flask_babel import lazy_gettext
from config.items.default import Item


class Dropdown(Item):
    """
    Dropdown item subclass
    """

    TYPE = "dropdown"
    VISIBLE = False
    NAME = lazy_gettext("Dropdown")
    DESCRIPTION = lazy_gettext("Pick a one from multiple options")
