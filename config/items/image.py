from flask_babel import gettext
from config.items.default import Item


class Image(Item):
    """
    Image item subclass
    """

    TYPE = "image"
    VISIBLE = True
    NAME = gettext("Image")
    PROTOCOLS_ABLE = ["rtsp", "mqtt"]

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
            self._URL: "",
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label")),
            self._URL: Input().make_object(value=self.config[self._URL], label=gettext("URL"))
        }

    # def on_display_value(self, value, config=None):
    #     from requests.auth import HTTPDigestAuth
    #     import requests
    #     import base64
    #
    #     request = requests.get("http://172.16.0.30:65001/ISAPI/Streaming/channels/102/picture", auth=HTTPDigestAuth("aa", "aa"))
    #
    #     base64_encoded = base64.b64encode(request.content).decode("utf-8")
    #     content = "data:image/jpeg;base64,{}".format(base64_encoded)
    #     print("loading")
    #     return content

