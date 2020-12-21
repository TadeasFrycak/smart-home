from flask_babel import lazy_gettext
from config.items.default import Item


class Toggle(Item):
    """
    Toggle item subclass
    """

    TYPE = "toggle"
    VISIBLE = True
    NAME = lazy_gettext("Toggle")
    DESCRIPTION = lazy_gettext("Toggle value - on/off")
    VALUE = False

    @property
    def config(self):
        return {
            self._LABEL: lazy_gettext("Toggle"),
            self._PLACEHOLDER: "",
            self._DISABLED: False
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=lazy_gettext("Label")),
            self._PLACEHOLDER: Input().make_object(value=self.config[self._PLACEHOLDER], label=lazy_gettext("Placeholder")),
            self._DISABLED: self.make_object(value=self.config[self._DISABLED], label=lazy_gettext("Disabled"))
        }
