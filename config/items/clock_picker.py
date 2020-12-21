from flask_babel import lazy_gettext
from config.items.default import Item


class ClockPicker(Item):
    """
    ClockPicker item subclass
    """

    TYPE = "clock_picker"
    VISIBLE = True
    NAME = lazy_gettext("Clock picker")
    VALUE = ""

    @property
    def config(self):
        return {
            self._PLACEHOLDER: lazy_gettext("Click to set the time..."),
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._PLACEHOLDER: Input().make_object(value=self.config[self._PLACEHOLDER], label=lazy_gettext("Placeholder"))
        }
