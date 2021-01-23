from flask_babel import gettext
from config.items.default import Item


class Toggle(Item):
    """
    Toggle item subclass
    """

    TYPE = "toggle"
    VISIBLE = True
    NAME = gettext("Toggle")
    DESCRIPTION = gettext("Toggle value - on/off")
    VALUE = False

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._PLACEHOLDER: "",
            self._DISABLED: False
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._PLACEHOLDER: Input().make_object(value=self.config[self._PLACEHOLDER], label=gettext("Placeholder")),
            self._DISABLED: self.make_object(value=self.config[self._DISABLED], label=gettext("Disabled"))
        }
