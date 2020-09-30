import configparser
import json
import glob
import os


class FileManager:
    """
    File Manager class
    """

    DATA_DIR = "data"
    SERVER_CONFIG_DIR = "server_config"
    APP_CONFIG_DIR = "app_config"
    TEMPLATES_DIR = "templates"

    DEVICES_FILE = "devices.json"
    WHITELIST_FILE = "whitelist.json"
    BLACKLIST_FILE = "blacklist.json"
    SETTINGS_FILE = "settings.json"
    MAC_LIST_FILE = "mac_list.json"

    CHARSET = "utf-8"
    
    def __init__(self):
        """
        Init of class FileManager class
        """

        self.__devices = None
        self.__settings = None
        self.__img_data = None

    def load_file(self, path=None):
        """
        Load value
        :param path: path to value
        :return:
        """

        with open(path, mode="r", encoding=self.CHARSET) as f:
            if "json" in path:
                data = json.load(f)
                
            else:
                data = f.read()

        return data

    def write_file(self, path, data, is_json):
        """
        Write to value
        :param path: path to value
        :param data: data
        :param is_json: is file JSON?
        :return:
        """

        with open(path, mode="w", encoding=self.CHARSET) as f:
            if is_json is True:
                json.dump(data, f)

            else:
                f.write(data)

    @staticmethod
    def get_filename_from_path(path):
        return os.path.basename(path)

    def list_file_names(self, path=None, name="*.*", extension=True, full_path=False):
        """
        List all file names in folder
        :param path: folder to list files
        :param name: filter of file name
        :param extension: get files with extension
        :param full_path: get files with full path
        :return:
        """

        data = []

        for i in glob.glob(pathname=self.path_join(path, name)):
            if full_path is False:
                data.append(self.get_filename_from_path(i))

            else:
                data.append(i)

        for num, i in enumerate(data):
            if extension is False:
                data[num] = os.path.splitext(i)[0]

            else:
                break

        return data

    @property
    def config(self):
        """
        Get classify config JSON
        :return:
        """
        config = configparser.ConfigParser()
        config.read("config/main.ini")
        return config

    @property
    def settings(self):
        """
        Get settings
        :return:
        """

        if self.__settings is None:
            self.__settings = self.load_file(path=self.path_join(self.DATA_DIR, self.APP_CONFIG_DIR,
                                                                 self.SETTINGS_FILE))

        return self.__settings

    @property
    def devices(self):
        """
        Get devices
        :return:
        """

        if self.__devices is None:
            self.__devices = self.load_file(path=self.path_join(self.DATA_DIR, self.APP_CONFIG_DIR, self.DEVICES_FILE))

        return self.__devices

    @devices.setter
    def devices(self, devices):
        """
        Set devices
        :param devices: devices to write
        :return:
        """

        self.__devices = devices
        self.write_file("data/app_config/devices.json", devices, True)

    @property
    def img_data(self):
        if self.__img_data is None:
            self.__img_data = self.load_file(path=self.path_join(self.DATA_DIR, "img_data.json"))

        return self.__img_data

    @img_data.setter
    def img_data(self, data):
        self.__img_data = data
        self.write_file(path=self.path_join(self.DATA_DIR, "img_data.json"), data=data, is_json=True)

    @property
    def whitelist(self):
        """
        Get whitelist JSON
        :return:
        """

        return self.load_file(path=self.path_join(self.DATA_DIR, self.APP_CONFIG_DIR, self.WHITELIST_FILE))

    @property
    def blacklist(self):
        """
        Get blacklist JSON
        :return:
        """

        return self.load_file(path=self.path_join(self.DATA_DIR, self.APP_CONFIG_DIR, self.BLACKLIST_FILE))

    @property
    def mac_list(self):
        """
        Get MAC list JSON
        :return:
        """

        return self.load_file(path=self.path_join(self.DATA_DIR, self.MAC_LIST_FILE))

    @mac_list.setter
    def mac_list(self, mac_list):
        """
        Get MAC list JSON
        :return:
        """

        self.write_file(path=self.path_join(self.DATA_DIR, self.MAC_LIST_FILE), data=mac_list, is_json=True)

    def get_latest_apk(self):
        apks = self.list_file_names(path="static/android", name="*.apk")
        apks.sort()
        return apks[-1]

    @staticmethod
    def path_join(*argv):
        """
        Join paths to one
        :param argv: paths
        :return:
        """

        return "/".join(argv)  # os.path.join(*argv)
