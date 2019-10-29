import json
import os


class FileManager:
    """
    File Manager
    """

    CONFIG_DIR = "config"
    CONFIG_JSON = "main.json"
    CONFIG_DEVICES = "devices.json"
    CONFIG_ITEMS = "items.json"

    TEMPLATES_DIR = "templates"
    
    def __init__(self):
        """
        Init of class FileManager
        """

        self.config_data = None
        self.devices_data = None
        self.items_data = None
        
        # self.root_dir = os.path.dirname(sys.modules["__main__"].__file__)

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
        f = open(path, "w")

        if is_json is True:
            json.dump(data, f)

        else:
            f.write(data)

        f.close()

    def config(self, overwrite=False):
        """
        Get config
        :param overwrite: overwrite?
        :return:
        """

        if self.config_data is None or overwrite is True:
            self.config_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_JSON), is_json=True)

        return self.config_data

    def devices(self, overwrite=False):
        """
        Get devices
        :param overwrite: overwrite?
        :return:
        """

        if self.devices_data is None or overwrite is True:
            self.devices_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_DEVICES), is_json=True)
            
        return self.devices_data

    def items(self, overwrite=False):
        """
        Get items
        :param overwrite: overwrite?
        :return:
        """

        if self.items_data is None or overwrite is True:
            self.items_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_ITEMS), is_json=True)
            
        return self.items_data

    @staticmethod
    def path_join(path1, path2):
        """
        Join two paths
        :param path1: path one
        :param path2: path two
        :return:
        """

        return os.path.join(path1, path2)
