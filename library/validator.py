import json


class Validator:
    """
    Validator class
    """

    def __init__(self, fmng, tmng):
        """
        Init of Validator
        :param fmng: file_manager
        :param tmng: template_manager
        """

        self.__fmng = fmng
        self.__tmng = tmng

    def validate_jsons(self):
        """
        Validate JSONs
        :return: True/exception
        """

        try:
            with open(self.__fmng.path_join(self.__fmng.CONFIG_DIR, self.__fmng.CONFIG_DEVICES), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.CONFIG_DIR, self.__fmng.CONFIG_ITEMS), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.CONFIG_DIR, self.__fmng.CONFIG_JSON), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.CONFIG_DIR, self.__fmng.CONFIG_WHITELIST), "r") as f:
                json.load(f)

        except Exception as e:
            return e

        else:
            return True

    def check_duplicity_ids(self):
        """
        Check duplicity IDs of modal and tiles
        :return:
        """

        # Check duplicity for tiles
        for page, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            IDs = []

            for device in self.__fmng.devices()[self.__tmng.ITEMS][page][self.__tmng.DATA]:
                # Check duplicity for current device
                if device[self.__tmng.DATA][self.__tmng.ID] not in IDs:
                    IDs.append(device[self.__tmng.DATA][self.__tmng.ID])

                else:
                    return device

        # Check duplicity for items in modals
        for page, page_content in enumerate(self.__fmng.devices()[self.__tmng.ITEMS]):
            for device in self.__fmng.devices()[self.__tmng.ITEMS][page][self.__tmng.DATA]:
                try:
                    IDs = []
                    for modal_item in device[self.__tmng.MODAL]:
                        if modal_item[self.__tmng.DATA][self.__tmng.ID] not in IDs:
                            IDs.append(modal_item[self.__tmng.DATA][self.__tmng.ID])

                        else:
                            return device

                except Exception as e:
                    pass

        return True
