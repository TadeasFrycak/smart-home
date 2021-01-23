from config.tiles.value_double import ValueDouble
from config.tiles.alarm_clock import AlarmClock
from config.tiles.toggle import Toggle
from config.tiles.player import Player
from config.tiles.blank import Blank
from config.tiles.value import Value


class Tiles:
    INSTANCES = [
        ValueDouble(),
        AlarmClock(),
        Player(),
        Toggle(),
        Value(),
        Blank()
    ]

    DEFAULT_TILE_TYPE = "blank"

    def __init__(self):
        pass

    def get_tile_edit_objects(self):
        tiles = {}
        for instance in self.INSTANCES:
            tile_object = instance.make_full_object()
            tiles[tile_object["type"]] = tile_object

        return tiles

    def get_object(self, tile_type):
        for instance in self.INSTANCES:
            if tile_type == instance.TYPE:
                return instance

    def get_default(self):
        return self.get_object(self.DEFAULT_TILE_TYPE).make_object()
