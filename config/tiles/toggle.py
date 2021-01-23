from flask_babel import gettext
from config.tiles.default import Tile


class Toggle(Tile):
    """
    Toggle tile subclass
    """

    TYPE = "toggle"
    VISIBLE = True
    NAME = gettext("Toggle")
    VALUE = False

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
