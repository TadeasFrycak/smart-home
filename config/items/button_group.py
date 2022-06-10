from flask_babel import gettext
from config.items.default import Item


class ButtonGroup(Item):
    """
    ButtonGroup item subclass
    """

    TYPE = "button_group"
    VISIBLE = True
    NAME = gettext("Button group")
    PROTOCOLS_ABLE = ["mqtt"]

    VALUE = "second"

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._CHECKBOX: False,
            self._OPTIONS: [
                ["first",    gettext("First")],
                [self.VALUE, gettext("Second")],
                ["third",    gettext("Third")]
            ]
        }

    @property
    def edit_config(self):
        from config.items.input import Input
        from config.items.toggle import Toggle
        # TODO lepší bude asi jen inicializovat daný type jednou a poté už jen vytvářet objekty
        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            # TODO sem dát místo Toggle BTN group
            self._CHECKBOX: Toggle().make_object(value=self.config[self._CHECKBOX], placeholder="Default is radio",
                                                 label=gettext("Checkbox mode (RR)")),
            self._OPTIONS: Input().make_object(value=self.config[self._OPTIONS], placeholder=gettext("Option"),
                                               list=True, count=2, label=gettext("Options (RR)"))
        }
