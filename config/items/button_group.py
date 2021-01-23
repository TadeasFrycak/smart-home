from flask_babel import gettext
from config.items.default import Item


class ButtonGroup(Item):
    """
    ButtonGroup item subclass
    """

    TYPE = "button_group"
    VISIBLE = True
    NAME = gettext("Button group")
    DESCRIPTION = gettext("Toggle/Radio")

    VALUE = gettext("Second")

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._BUTTONS: True,
            self._CHECKBOX: False,
            self._OPTIONS: [
                gettext("First"),
                self.VALUE,
                gettext("Third"),
            ]
        }

    @property
    def edit_config(self):
        from config.items.input import Input
        from config.items.toggle import Toggle
        # TODO lepší bude asi jen inicializovat daný type jednou a poté už jen vytvářet objekty
        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._BUTTONS: Toggle().make_object(value=self.config[self._BUTTONS], placeholder="Default is buttons",
                                                label=gettext("Use buttons (RR)")),
            self._CHECKBOX: Toggle().make_object(value=self.config[self._CHECKBOX], placeholder="Default is radio",
                                                 label=gettext("Checkbox mode (RR)")),
            self._OPTIONS: Input().make_object(value=self.config[self._OPTIONS], placeholder=gettext("Option"),
                                               list=True, label=gettext("Options (RR)"))
        }
