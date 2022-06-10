from flask_babel import gettext
from config.items.default import Item


class Input(Item):
    """
    Input item subclass
    """

    TYPE = "input"
    VISIBLE = True
    NAME = gettext("Input")
    PROTOCOLS_ABLE = ["mqtt"]
    VALUE = ""

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._PLACEHOLDER: "",
            self._PREPEND: "",
            self._COUNT: 1,
            self._MAX_LENGTH: 40,
            self._READONLY: False,
            self._NUMBER: False,
            self._INVALID: False,
            self._LIST: False,
            self._BUTTON: False

        }

    @property
    def edit_config(self):
        from config.items.toggle import Toggle
        from config.items.slider import Slider

        return {
            self._LABEL: self.make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._PLACEHOLDER: self.make_object(value=self.config[self._PLACEHOLDER], label=gettext("Placeholder")),
            self._PREPEND: self.make_object(value=self.config[self._PREPEND], label=gettext("Prepend text")),
            self._COUNT: Slider().make_object(value=self.config[self._COUNT], min=1, max=4, step=1, suffix="", label=gettext("Inputs count (RR)")),
            self._READONLY: Toggle().make_object(value=self.config[self._READONLY], label=gettext("Readonly")),
            self._LIST: Toggle().make_object(value=self.config[self._LIST], label=gettext("Value list (RR)")),
            # self._INVALID: Toggle().make_object(value=self.config[self._INVALID], label=gettext("Invalid")),
            self._NUMBER: Toggle().make_object(value=self.config[self._NUMBER], label=gettext("Number")),
            self._BUTTON: Toggle().make_object(value=self.config[self._BUTTON], label=gettext("Confirm button"))
        }
