from flask_babel import gettext
from config.items.default import Item


class DateRangePicker(Item):
    """
    DateRangePicker item subclass
    """

    TYPE = "date_range_picker"
    VISIBLE = False
    NAME = gettext("Date picker")
    DESCRIPTION = gettext("Pick a date or date range")

    @property
    def config(self):
        return {
            self._RANGE: True
        }

    @property
    def edit_config(self):
        from config.items.toggle import Toggle

        return {
            self._RANGE: Toggle().make_object(value=self.config[self._RANGE],
                                              label=gettext("Range"))
        }