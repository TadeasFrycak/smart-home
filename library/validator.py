import json


class Validator:
    """
    Validator class
    """

    def __init__(self, fmng, tmng_r):
        """
        Init of Validator
        :param fmng: file_manager
        :param tmng_r: template_manager
        """

        self.__fmng = fmng
        self.__tmng_r = tmng_r

    def validate_jsons(self):
        """
        Validate JSONs
        :return: True/exception
        """

        try:
            with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.APP_CONFIG_DIR,
                                            self.__fmng.DEVICES_FILE), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.SERVER_CONFIG_DIR,
                                            self.__fmng.CONFIG_FILE), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.APP_CONFIG_DIR,
                                            self.__fmng.WHITELIST_FILE), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.APP_CONFIG_DIR,
                                            self.__fmng.BLACKLIST_FILE), "r") as f:
                json.load(f)

            with open(self.__fmng.path_join(self.__fmng.DATA_DIR, self.__fmng.MAC_LIST_FILE), "r") as f:
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
        for page, page_content in enumerate(self.__fmng.devices):
            IDs = []

            for device in page_content[self.__tmng_r.DATA]:
                # Check duplicity for current device
                if device[self.__tmng_r.DATA][self.__tmng_r.ID] not in IDs:
                    IDs.append(device[self.__tmng_r.DATA][self.__tmng_r.ID])

                else:
                    return device

        # Check duplicity for items in modals
        for page, page_content in enumerate(self.__fmng.devices):
            for device in page_content[self.__tmng_r.DATA]:
                try:
                    IDs = []
                    for modal_item in device[self.__tmng_r.MODAL]:
                        if modal_item[self.__tmng_r.DATA][self.__tmng_r.ID] not in IDs:
                            IDs.append(modal_item[self.__tmng_r.DATA][self.__tmng_r.ID])

                        else:
                            return device

                except Exception as e:
                    pass

        return True
