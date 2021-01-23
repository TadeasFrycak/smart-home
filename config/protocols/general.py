from config.protocols.magic_packet import MagicPacket
from config.protocols.mqtt import MQTT
from config.protocols.timer import Timer


class Protocols:
    def __init__(self, terminal, updater, fmng, tmng_r):
        self.__updater = updater
        self.__fmng = fmng
        self.__tmng_r = tmng_r

        self.__instances = [
            MQTT(terminal, self),
            MagicPacket(terminal, self),
            Timer(terminal, self)
        ]

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

    def update(self, protocol_type, value, config_part):
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
                            self.__updater.tile_value(tile["id"], value)
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
                                self.__updater.item_value(tile_id=tile["id"], item_id=item["id"], value=value)
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
