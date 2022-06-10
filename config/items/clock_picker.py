from flask_babel import gettext
from config.items.default import Item


class ClockPicker(Item):
    """
    ClockPicker item subclass
    """

    TYPE = "clock_picker"
    VISIBLE = True
    NAME = gettext("Clock picker")
    PROTOCOLS_ABLE = ["mqtt"]

    VALUE = ""

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._PLACEHOLDER: gettext("Click to set the time...")
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._PLACEHOLDER: Input().make_object(value=self.config[self._PLACEHOLDER], label=gettext("Placeholder"))
        }
