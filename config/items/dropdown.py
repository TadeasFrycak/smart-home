from flask_babel import gettext
from config.items.default import Item


class Dropdown(Item):
    """
    Dropdown item subclass
    """

    TYPE = "dropdown"
    VISIBLE = True
    NAME = gettext("Dropdown")
    DESCRIPTION = gettext("Pick an option")

    VALUE = gettext("Second")

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._OPTIONS: [
                gettext("First"),
                self.VALUE,
                gettext("Third"),
            ]
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._OPTIONS: Input().make_object(value=self.config[self._OPTIONS], placeholder=gettext("Option"),
                                               list=True, label=gettext("Options (RR)"))
        }
