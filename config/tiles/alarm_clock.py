from flask_babel import gettext
from config.tiles.default import Tile


class AlarmClock(Tile):
    """
    Alarm Clock tile subclass
    """

    TYPE = "alarm_clock"
    VISIBLE = True
    NAME = gettext("Alarm Clock")
    PROTOCOLS_ABLE = ["mqtt", "magic_packet", "alarm"]
    VALUE = {"main": False, "monday": False, "tuesday": False, "wednesday": False, "thursday": False, "friday": False,
             "saturday": False, "sunday": False}

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
