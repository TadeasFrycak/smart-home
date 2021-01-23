from flask_babel import gettext
from config.items.default import Item


class Slider(Item):
    """
    Slider item subclass
    """

    TYPE = "slider"
    VISIBLE = True
    NAME = gettext("Slider")
    DESCRIPTION = gettext("Slide to set value")
    VALUE = [50, 80]

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._SUFFIX: "%",
            self._MIN: 0,
            self._MAX: 100,
            self._STEP: 5,
            self._SMOOTH: False,
            self._RANGE: False,
            self._DISABLED: False
        }

    @property
    def edit_config(self):
        from config.items.input import Input
        from config.items.toggle import Toggle

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._SUFFIX: Input().make_object(value=self.config[self._SUFFIX], label=gettext("Suffix")),
            self._MIN: Input().make_object(value=self.config[self._MIN], label=gettext("Minimal value")),
            self._MAX: Input().make_object(value=self.config[self._MAX], label=gettext("Maximal value")),
            self._STEP: Input().make_object(value=self.config[self._STEP], label=gettext("Step value")),
            self._SMOOTH: Toggle().make_object(value=self.config[self._SMOOTH], label=gettext("Smooth")),
            self._RANGE: Toggle().make_object(value=self.config[self._RANGE], label=gettext("Range")),
            self._DISABLED: Toggle().make_object(value=self.config[self._DISABLED], label=gettext("Disabled"))
        }
