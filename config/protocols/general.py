from config.protocols.magic_packet import MagicPacket
from config.protocols.mqtt import MQTT
from config.protocols.rtsp import RTSP
# from config.protocols.prusa import Prusa
from config.protocols.timer import Alarm


class Protocols:
    def __init__(self, terminal, updater, fmng, tmng_r):
        self.updater = updater
        self.__fmng = fmng
        self.__tmng_r = tmng_r

        self.__instances = [
            MagicPacket(terminal, self),
            MQTT(terminal, self),
            Alarm(terminal, self),
            RTSP(terminal, self)
            # Prusa(terminal, self)
        ]

    def get_tile_value(self, tile_id):
        tile = self.__tmng_r.get_tile(tile_id)

        if tile:
            return tile["value"]

    def get_item_value(self, tile_id, item_id):
        item = self.__tmng_r.get_item(tile_id, item_id)

        if item:
            return item["value"]

    def get_count(self, protocol_type, config):
        number = 0
        for page in self.__fmng.devices:
            # Get tiles (number and content)
            for tile in page[self.__tmng_r.CHILDREN]:
                for protocol in tile["protocols"]:
                    if protocol["type"] == protocol_type:
                        if protocol["config"] == config:
                            number += 1

                for item in tile["modal"]:
                    for protocol in item["protocols"]:
                        if protocol["type"] == protocol_type and protocol["config"] == config:
                            number += 1
        return number

    def config(self, protocol_type, tile_id, item_id=None):
        # Get pages (number and content)
        for page in self.__fmng.devices:
            # Get tiles (number and content)
            for tile in page[self.__tmng_r.CHILDREN]:
                if item_id:
                    for item in tile["modal"]:
                        for protocol in item["protocols"]:
                            if protocol["type"] == protocol_type:
                                return protocol["config"]

                else:
                    for protocol in tile["protocols"]:
                        if protocol["type"] == protocol_type:
                            return protocol["config"]

    def update(self, protocol_type, value, config_part, save=True):
        # Get pages (number and content)
        for page in self.__fmng.devices:
            # Get tiles (number and content)
            for tile in page[self.__tmng_r.CHILDREN]:
                for protocol in tile["protocols"]:
                    if protocol["type"] == protocol_type:
                        can = []
                        for protocol_value in config_part:
                            if protocol_value in protocol["config"]:
                                if protocol["config"][protocol_value] == config_part[protocol_value]:
                                    can.append(True)
                                else:
                                    can.append(False)
                            else:
                                can.append(False)

                        if all(can):
                            if self.updater.tile_value(tile["id"], value, save=save):
                                for protocol_inner in tile["protocols"]:
                                    if protocol_inner["type"] != protocol_type:
                                        self.get_object(protocol_inner["type"]).publish(protocol_inner["config"], value)
                                break

                for item in tile["modal"]:
                    for protocol in item["protocols"]:
                        if protocol["type"] == protocol_type:
                            can = []
                            for protocol_value in config_part:
                                if protocol_value in protocol["config"]:
                                    if protocol["config"][protocol_value] == config_part[protocol_value]:
                                        can.append(True)
                                    else:
                                        can.append(False)
                                else:
                                    can.append(False)

                            if all(can):
                                if self.updater.item_value(tile_id=tile["id"], item_id=item["id"], value=value, save=save):
                                    for protocol_inner in item["protocols"]:
                                        if protocol_inner["type"] != protocol_type:
                                            self.get_object(protocol_inner["type"]).publish(protocol_inner["config"], value)
                                    break

    def get_protocol_edit_objects(self):
        items = {}
        for instance in self.__instances:
            item_object = instance.make_full_object()
            items[item_object["type"]] = item_object

        return items

    def get_object(self, protocol_type):
        for instance in self.__instances:
            if protocol_type == instance.TYPE:
                return instance
