import json
import os


class FileManager:
    """
    File Manager class
    """

    CONFIG_DIR = "config"
    CONFIG_JSON = "main.json"
    CONFIG_DEVICES = "devices.json"
    CONFIG_ITEMS = "items.json"
    CONFIG_WHITELIST = "whitelist.json"

    TEMPLATES_DIR = "templates"
    
    def __init__(self):
        """
        Init of class FileManager class
        """

        self.__config_data = None
        self.__devices_data = None
        self.__items_data = None
        self.__whitelist_data = None

        # self.root_dir = os.path.dirname(sys.modules["__main__"].__file__)

    def reload_files(self):
        """
        Set all files data to None
        :return:
        """

        self.__config_data = None
        self.__devices_data = None
        self.__items_data = None
        self.__whitelist_data = None

    @staticmethod
    def load_file(path, is_json):
        """
        Load file
        :param path: path to file
        :param is_json: is json?
        :return:
        """

        f = open(path, "r")
        
        if is_json is True:
            data = json.load(f)
                
        else:
            data = "".join(f.readlines())
                
        f.close()
        return data

    @staticmethod
    def write_file(path, data, is_json):
        """
        Write to file
        :param path: path to file
        :param data: data
        :param is_json: is JSON?
        :return:
        """

        f = open(path, "w")

        if is_json is True:
            json.dump(data, f)

        else:
            f.write(data)

        f.close()

    def write_devices(self, path, data, is_json):
        """
        Write to RAM
        :param path: old
        :param data: data
        :return:
        """
        self.__devices_data = data

    def config(self, overwrite=False):
        """
        Get config
        :param overwrite: overwrite?
        :return:
        """

        if self.__config_data is None or overwrite is True:
            self.__config_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_JSON), is_json=True)

        return self.__config_data

    def devices(self, overwrite=False):
        """
        Get devices
        :param overwrite: overwrite?
        :return:
        """

        if self.__devices_data is None or overwrite is True:
            self.__devices_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_DEVICES), is_json=True)
            
        return self.__devices_data

    def items(self, overwrite=False):
        """
        Get items
        :param overwrite: overwrite?
        :return:
        """

        if self.__items_data is None or overwrite is True:
            self.__items_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_ITEMS), is_json=True)
            
        return self.__items_data

    def whitelist(self, overwrite=False):
        """
        Get whitelist
        :param overwrite: overwrite?
        :return:
        """

        if self.__whitelist_data is None or overwrite is True:
            self.__whitelist_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_WHITELIST),
                                                   is_json=True)

        return self.__whitelist_data

    @staticmethod
    def path_join(path1, path2):
        """
        Join two paths
        :param path1: path one
        :param path2: path two
        :return:
        """

        return os.path.join(path1, path2)
