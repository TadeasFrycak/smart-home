from flask_babel import lazy_gettext
from config.items.default import Item


class Input(Item):
    """
    Input item subclass
    """

    TYPE = "input"
    VISIBLE = True
    NAME = lazy_gettext("Input")
    DESCRIPTION = lazy_gettext("Field for free typing")
    VALUE = ""

    @property
    def config(self):
        return {
            self._LABEL: lazy_gettext("Input"),
            self._PLACEHOLDER: "",
            self._READONLY: False,
            self._INVALID: False,
            self._BUTTON: False
        }

    @property
    def edit_config(self):
        from config.items.toggle import Toggle

        return {
            self._LABEL: self.make_object(value=self.config[self._LABEL], label=lazy_gettext("Label")),
            self._PLACEHOLDER: self.make_object(value=self.config[self._PLACEHOLDER], label=lazy_gettext("Placeholder")),
            self._READONLY: Toggle().make_object(value=self.config[self._READONLY], label=lazy_gettext("Readonly")),
            self._INVALID: Toggle().make_object(value=self.config[self._INVALID], label=lazy_gettext("Invalid")),
            self._BUTTON: Toggle().make_object(value=self.config[self._BUTTON], label=lazy_gettext("Confirm button (refresh required)"))
        }
