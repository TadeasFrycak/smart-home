from flask_babel import lazy_gettext
from config.items.default import Item


class DateRangePicker(Item):
    """
    DateRangePicker item subclass
    """

    TYPE = "date_range_picker"
    VISIBLE = True
    NAME = lazy_gettext("Date picker")
    DESCRIPTION = lazy_gettext("Pick a date or date range")

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
                                              label=lazy_gettext("Range"))
        }