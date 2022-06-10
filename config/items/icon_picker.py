from flask_babel import gettext
from config.items.default import Item


class IconPicker(Item):
    """
    Icon picker item subclass
    """

    TYPE = "icon_picker"
    VISIBLE = False
    NAME = gettext("Icon picker")
    PROTOCOLS_ABLE = ["mqtt"]
    VALUE = "none.png"

    ICON_PATH = "static/img/icons"

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            "icons": self._fmng.list_file_names(path=self.ICON_PATH)
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
        }
