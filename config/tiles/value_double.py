from flask_babel import gettext
from config.tiles.default import Tile


class ValueDouble(Tile):
    """
    Value Double tile subclass
    """

    TYPE = "value_double"
    VISIBLE = True
    NAME = gettext("Value Double")
    PROTOCOLS_ABLE = ["mqtt"]
    VALUE = {"left": {"value": "Null", "suffix": ""}, "right": {"value": "Null", "suffix": ""}}

    @property
    def config(self):
        return {
            self._ICON: "none.png"
        }

    @property
    def edit_config(self):
        from config.items.icon_picker import IconPicker

        return {
            self._ICON: IconPicker().make_object(value=self.config[self._ICON], label=gettext("Tile icon")),
        }
