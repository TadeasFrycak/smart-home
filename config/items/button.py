from flask_babel import gettext
from config.items.default import Item


class Button(Item):
    """
    Button item subclass
    """

    TYPE = "button"
    VISIBLE = True
    NAME = gettext("Button")
    PROTOCOLS_ABLE = ["mqtt", "magic_packet", "alarm"]
    VALUE = False

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._COLOR: "info",
            self._ON_VALUE: 1
        }

    @property
    def edit_config(self):
        from config.items.input import Input
        from config.items.dropdown import Dropdown

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._COLOR: Dropdown().make_object(
                value=self.config[self._COLOR], label=gettext("Color"),
                options=["light", "secondary", "dark", "success", "primary", "info", "danger", "warning"]),
            self._ON_VALUE: Input().make_object(value=self.config[self._ON_VALUE], label=gettext("Value")),
        }
