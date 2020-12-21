from flask_babel import lazy_gettext
from config.items.default import Item


class Graph(Item):
    """
    Graph item subclass
    """

    TYPE = "graph"
    VISIBLE = False
    NAME = lazy_gettext("Graph")

    THRESHOLD = 5

    @property
    def config(self):
        return {
            self._LABEL: lazy_gettext("Graph"),
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=lazy_gettext("Label"))
        }

    def on_display_value(self, value):
        previous_value = value["y"][0]
        values_x = []
        values_y = []
        average = []
        for num, i in enumerate(value["y"]):
            if num % 50 == 49:
                # if abs(previous_value-i) > self.THRESHOLD:
                # print(abs(previous_value-i))
                current_value = sum(average)/len(average)
                values_y.append(current_value)
                values_x.append(value["x"][num])
                average = []
                # previous_value = current_value
            else:
                average.append(i)

        return {"x": values_x, "y": values_y}
