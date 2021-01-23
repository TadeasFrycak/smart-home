from flask_babel import gettext, lazy_gettext
from config.items.default import Item


class Button(Item):
    """
    Button item subclass
    """

    TYPE = "button"
    VISIBLE = True
    NAME = lazy_gettext("Button")
    VALUE = False

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._COLOR: "info",
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=lazy_gettext("Label")),
            self._COLOR: Input().make_object(value=self.config[self._COLOR], label=lazy_gettext("Color"))
        }
