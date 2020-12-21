from flask_babel import lazy_gettext
from config.items.default import Item


class ProgressBar(Item):
    """
    ProgressBar item subclass
    """

    TYPE = "progress_bar"
    VISIBLE = True
    NAME = lazy_gettext("Progress bar")
    VALUE = 50

    @property
    def config(self):
        return {
            self._LABEL: lazy_gettext("Progress bar"),
            self._MAX: 100,
            self._MIN: 0,
            self._COLOR: "info"
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=lazy_gettext("Label")),
            self._MAX: Input().make_object(value=self.config[self._MAX], label=lazy_gettext("Maximal value")),
            self._MIN: Input().make_object(value=self.config[self._MIN], label=lazy_gettext("Minimal value")),
            self._COLOR: Input().make_object(value=self.config[self._COLOR], label=lazy_gettext("Color"))
        }