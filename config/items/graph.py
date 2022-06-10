import copy
import datetime
import math
import time

from flask_babel import gettext
from config.items.default import Item


class Graph(Item):
    """
    Graph item subclass
    """

    TYPE = "graph"
    VISIBLE = True
    NAME = gettext("Graph")
    PROTOCOLS_ABLE = ["mqtt"]

    THRESHOLD = 0.5

    VALUE = {"x": [], "y": []}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def config(self):
        return {
            self._LABEL: self.NAME,
        }

    @property
    def edit_config(self):
        from config.items.input import Input

        return {
            self._LABEL: Input().make_object(value=self.config[self._LABEL], label=gettext("Label"))
        }

    # def on_display_value(self, value):
    #     previous_value = value["y"][0]
    #
    #     values_x = []
    #     values_y = []
    #     differences_y = []
    #
    #     # Threshold
    #     for num, i in enumerate(value["y"]):
    #         if abs(previous_value-i) > self.THRESHOLD:
    #             current_value = i
    #             values_y.append(current_value)
    #             values_x.append(value["x"][num])
    #             previous_value = current_value
    #
    #     for num in range(len(values_y)-1):
    #         differences_y.append(round(abs(values_y[num]-values_y[num+1]), 12))
    #
    #     for j in range(1):
    #         for num in range(len(differences_y)-1):
    #             if differences_y[num] != "x" and differences_y[num+1] != "x":
    #                 old_while_num = abs(differences_y[num]-differences_y[num+1])
    #                 while_num = old_while_num
    #                 list_num = num
    #                 first = True
    #                 while abs(old_while_num - while_num) < 0.05:
    #                     while_num = abs(differences_y[list_num] - differences_y[list_num + 1])
    #                     if list_num + 1 < len(differences_y) - 1:
    #                         if not first:
    #                             differences_y[list_num] = "x"
    #                     else:
    #                         break
    #                     list_num += 1
    #                     first = False
    #                 else:
    #                     continue
    #         final_values_x = []
    #         final_values_y = []
    #         for num, i in enumerate(differences_y):
    #             if i != "x":
    #                 final_values_x.append(values_x[num])
    #                 final_values_y.append(values_y[num])
    #
    #         values_x = final_values_x
    #         values_y = final_values_y
    #
    #         differences_y = list(filter(lambda a: a != "x", differences_y))
    #
    #     print(final_values_y)
    #     print(differences_y)
    #     return {"x": final_values_x, "y": final_values_y}

    @staticmethod
    def diff_angle(point1, point2, point3):
        # print()
        # print(point1, point2, point3)
        dx1 = point2[0] - point1[0]
        dy1 = point2[1] - point1[1]
        dx2 = point3[0] - point1[0]
        dy2 = point3[1] - point1[1]

        angle1 = math.atan2(dy1, dx1)
        angle2 = math.atan2(dy2, dx2)
        # print(angle1, angle2)

        angle = math.degrees(abs(angle1 - angle2))
        return round(angle, 12)

    @staticmethod
    def convert_time(string):
        date_object = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(date_object.timetuple())

        return timestamp

    @staticmethod
    def on_new_value(before, current):
        if type(current) == dict:
            current = float(current["value"])
        new = copy.deepcopy(before)

        new_x = round(time.time())
        new_y = round(current)

        new["x"].append(new_x)
        new["y"].append(current)
        return new, {"x": new_x, "y": new_y}

    def on_display_value(self, value, config=None):
        # return value
        value = copy.deepcopy(value)
        return value
        bx = value["x"].copy()
        by = value["y"].copy()

        if not bx or not by:
            value["ox"] = []  # TODO remove this
            value["oy"] = []  # TODO remove this
            return value

        # TODO test this: https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
        value_x = []  # value["x"]  # [725:737]
        value_y = []  # value["y"]  # [725:737]

        previous_value = value["y"][0]
        # Threshold
        max_min = (max(value["y"]) - min(value["y"])) * 0.03
        a = time.time()
        for num, i in enumerate(value["y"]):
            if abs(previous_value-i) > max_min:
                current_value = i
                value_y.append(current_value)
                value_x.append(value["x"][num])
                previous_value = current_value
        final_x = [value_x[0]]
        final_y = [value_y[0]]
        print(time.time()-a)
        # return {"x": value_x, "y": value_y}
        i = 0
        addition_normal = 2
        addition = addition_normal

        while True:
            if i + addition < len(value_y):
                print(i, i+1, i+addition)
                diff = self.diff_angle([value_x[i],   value_y[i]],
                                       [value_x[i+1], value_y[i+1]],
                                       [value_x[i+2], value_y[i+2]])
                if diff == 0:
                    print(diff, "OK")
                    addition += 1

                else:
                    print(diff)
                    i += addition - addition_normal
                    addition = addition_normal
                    i += 1
                    print(i)
                    final_x.append(value_x[i])
                    final_y.append(value_y[i])

            else:
                final_x.append(value_x[len(value_x) - 1])
                final_y.append(value_y[len(value_y) - 1])
                break

        return {"x": final_x, "y": final_y, "ox": bx, "oy": by}

    # https://www.chartjs.org/docs/latest/axes/cartesian/time.html
    # def on_display_value(self, value):
    #     value_x = []  # value["x"]  # [725:737]
    #     value_y = []  # value["y"]  # [725:737]
    #
    #     previous_value = value["y"][0]
    #     # Threshold
    #     for num, i in enumerate(value["y"]):
    #         if abs(previous_value-i) > self.THRESHOLD:
    #             current_value = i
    #             value_y.append(current_value)
    #             value_x.append(value["x"][num])
    #             previous_value = current_value
    #
    #     # print(self.diff_angle([self.convert_time(value_x[0]), value_y[0]],
    #     #                       [self.convert_time(value_x[1]), value_y[1]],
    #     #                       [self.convert_time(value_x[2]), value_y[2]]))
    #     #
    #     # print(self.diff_angle([self.convert_time(value_x[3]), value_y[3]],
    #     #                       [self.convert_time(value_x[4]), value_y[4]],
    #     #                       [self.convert_time(value_x[5]), value_y[5]]))
    #     #
    #     # print(self.diff_angle([self.convert_time(value_x[4]), value_y[4]],
    #     #                       [self.convert_time(value_x[5]), value_y[5]],
    #     #                       [self.convert_time(value_x[6]), value_y[6]]))
    #     #
    #     # print(self.diff_angle([self.convert_time(value_x[6]), value_y[6]],
    #     #                       [self.convert_time(value_x[7]), value_y[7]],
    #     #                       [self.convert_time(value_x[8]), value_y[8]]))
    #
    #     final_x = [value_x[0]]
    #     final_y = [value_y[0]]
    #     # return {"x": value_x, "y": value_y}
    #     i = 0
    #     addition_normal = 2
    #     addition = addition_normal
    #
    #     while True:
    #         if i + addition < len(value_y):
    #             print(i, i+1, i+addition)
    #             diff = self.diff_angle([self.convert_time(value_x[i]),          value_y[i]],
    #                                    [self.convert_time(value_x[i+1]),        value_y[i+1]],
    #                                    [self.convert_time(value_x[i+addition]), value_y[i+addition]])
    #             if diff < 0.016:
    #                 print(diff, "OK")
    #                 addition += 1
    #
    #             else:
    #                 print(diff)
    #                 i += addition - addition_normal
    #                 addition = addition_normal
    #                 i += 1
    #                 print(i)
    #                 final_x.append(value_x[i])
    #                 final_y.append(value_y[i])
    #
    #
    #         else:
    #             final_x.append(value_x[len(value_x) - 1])
    #             final_y.append(value_y[len(value_y) - 1])
    #             break
    #
    #     # print()
    #     # print([":".join(a.split()[1].split(":")[0:2]) for a in value_x])
    #     # print(value_y)
    #     # print()
    #     # print([":".join(a.split()[1].split(":")[0:2]) for a in final_x])
    #     # print(final_y)
    #     return {"x": final_x, "y": final_y}
