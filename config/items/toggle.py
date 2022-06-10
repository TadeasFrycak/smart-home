from flask_babel import gettext
from config.items.default import Item


class Toggle(Item):
    """
    Toggle item subclass
    """

    TYPE = "toggle"
    VISIBLE = True
    NAME = gettext("Toggle")
    PROTOCOLS_ABLE = ["mqtt", "alarm"]
    VALUE = False

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._PLACEHOLDER: "",
            self._DISABLED: False,
            self._ON_VALUE: 1,
            self._OFF_VALUE: 0
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._ON_VALUE: Input().make_object(value=self.config[self._ON_VALUE], label=gettext("On value")),
            self._OFF_VALUE: Input().make_object(value=self.config[self._OFF_VALUE], label=gettext("Off value"))
            # self._PLACEHOLDER: Input().make_object(value=self.config[self._PLACEHOLDER], label=gettext("Placeholder")),
            # self._DISABLED: self.make_object(value=self.config[self._DISABLED], label=gettext("Disabled"))
        }
