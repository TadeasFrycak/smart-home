from flask_babel import gettext
from config.items.default import Item


class ProgressBar(Item):
    """
    ProgressBar item subclass
    """

    TYPE = "progress_bar"
    VISIBLE = True
    NAME = gettext("Progress bar")
    VALUE = 50

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._MAX: 100,
            self._MIN: 0,
            self._COLOR: "info"
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._MAX: Input().make_object(value=self.config[self._MAX], label=gettext("Maximal value")),
            self._MIN: Input().make_object(value=self.config[self._MIN], label=gettext("Minimal value")),
            self._COLOR: Input().make_object(value=self.config[self._COLOR], label=gettext("Color"))
        }
