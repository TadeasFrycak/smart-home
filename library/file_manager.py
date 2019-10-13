import json
import sys
import os

class FileManager:
    CONFIG_DIR = "config"
    CONFIG_JSON = "main.json"
    CONFIG_DEVICES = "devices.json"
    CONFIG_ITEMS = "items.json"

    TEMPLATES_DIR = "templates"
    
    def __init__(self):
        self.config_data = None
        self.devices_data = None
        self.items_data = None
        
        # self.root_dir = os.path.dirname(sys.modules["__main__"].__file__)

    def load_file(self, path, is_json):
        f = open(path)
        
        if is_json is True:
            data = json.load(f)
                
        else:
            data = "".join(f.readlines())
                
        f.close()
        return data

    def config(self, overwrite):
        if self.config_data is None or overwrite is True:
            self.config_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_JSON), is_json=True)

        return self.config_data

    def devices(self, overwrite):
        if self.devices_data is None or overwrite is True:
            self.devices_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_DEVICES), is_json=True)
            
        return self.devices_data

    def items(self, overwrite):
        if self.items_data is None or overwrite is True:
            self.items_data = self.load_file(path=self.path_join(self.CONFIG_DIR, self.CONFIG_ITEMS), is_json=True)
            
        return self.items_data

    def path_join(self, path1, path2):
        return os.path.join(path1, path2)
