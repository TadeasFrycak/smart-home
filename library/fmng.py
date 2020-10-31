import configparser
import json
import glob
import os


class FileManager:
    """
    File Manager class
    """

    DATA_DIR = "data"
    CONFIG_DIR = "config"
    TEMPLATES_DIR = "templates"
    TEMP_DIR = "temp"

    DEVICES_FILE = "devices.json"
    WHITELIST_FILE = "whitelist.ini"
    BLACKLIST_FILE = "blacklist.ini"
    MAC_LIST_FILE = "mac_list.json"

    BACKGROUNDS_FILE = "backgrounds_data.json"
    REFRESH_FILE = "refresh_data.json"

    CHARSET = "utf-8"
    
    def __init__(self):
        """
        Init of class FileManager class
        """

        self.__devices = None
        self.__backgrounds_data = None
        self.__refresh_data = None

    def load_file(self, path=None, default=None):
        """
        Load value
        :param default: default value
        :param path: path to value
        :return:
        """

        if default is None:
            default = []

        try:
            with open(path, mode="r", encoding=self.CHARSET) as f:
                if "json" in path:
                    data = json.load(f)

                else:
                    data = f.read()
        except FileNotFoundError:
            with open(path, mode="w+", encoding=self.CHARSET) as f:
                data = default
                json.dump(data, f)

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
    def devices(self):
        """
        Get devices
        :return:
        """

        if self.__devices is None:
            self.__devices = self.load_file(path=self.path_join(self.DATA_DIR, self.DEVICES_FILE))

        return self.__devices

    @devices.setter
    def devices(self, devices):
        """
        Set devices
        :param devices: devices to write
        :return:
        """

        self.__devices = devices
        self.write_file(self.path_join(self.DATA_DIR, self.DEVICES_FILE), devices, True)

    @property
    def backgrounds_data(self):
        if self.__backgrounds_data is None:
            self.__backgrounds_data = self.load_file(path=self.path_join(self.TEMP_DIR, self.BACKGROUNDS_FILE), default={})

        return self.__backgrounds_data

    @backgrounds_data.setter
    def backgrounds_data(self, data):
        self.__backgrounds_data = data
        self.write_file(path=self.path_join(self.TEMP_DIR, self.BACKGROUNDS_FILE), data=data, is_json=True)

    @property
    def refresh_data(self):
        if self.__refresh_data is None:
            self.__refresh_data = self.load_file(path=self.path_join(self.TEMP_DIR, self.REFRESH_FILE))

        return self.__refresh_data

    @refresh_data.setter
    def refresh_data(self, data):
        self.__refresh_data = data
        self.write_file(path=self.path_join(self.TEMP_DIR, self.REFRESH_FILE), data=data, is_json=True)

    @property
    def whitelist(self):
        """
        Get whitelist JSON
        :return:
        """

        return self.load_file(path=self.path_join(self.CONFIG_DIR, self.WHITELIST_FILE))

    @property
    def blacklist(self):
        """
        Get blacklist JSON
        :return:
        """

        return self.load_file(path=self.path_join(self.CONFIG_DIR, self.BLACKLIST_FILE))

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

        return os.path.join(*argv)  # "/".join(argv)
