from config.items.date_range_picker import DateRangePicker
from config.items.clock_picker import ClockPicker
from config.items.progress_bar import ProgressBar
from config.items.button_group import ButtonGroup
from config.items.icon_picker import IconPicker
from config.items.separator import Separator
from config.items.dropdown import Dropdown
from config.items.button import Button
from config.items.slider import Slider
from config.items.toggle import Toggle
from config.items.input import Input
from config.items.graph import Graph
from config.items.image import Image


class Items:
    INSTANCES = [
        DateRangePicker(),
        ClockPicker(),
        ButtonGroup(),
        ProgressBar(),
        IconPicker(),
        Separator(),
        Dropdown(),
        Button(),
        Slider(),
        Toggle(),
        Input(),
        Graph(),
        Image()
    ]

    def __init__(self):
        pass

    def get_item_edit_objects(self):
        items = {}
        for instance in self.INSTANCES:
            item_object = instance.make_full_object()
            items[item_object["type"]] = item_object

        return items

    def get_object(self, item_type):
        for instance in self.INSTANCES:
            if item_type == instance.TYPE:
                return instance

    # def get_item_names(self):
    #     names = []
    #
    #     for instance in self.INSTANCES:
    #         item_object = instance.make_full_object()
    #         if item_object["visible"] is True:
    #             names.append(item_object["name"])
    #
    #     return names
