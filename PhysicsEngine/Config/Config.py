from configparser import ConfigParser
import os

class Config:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.abspath(os.path.join(__file__, "..", "..", "..", "config.ini"))

        if not os.path.isfile(self.config_path):
            self.restore_to_default()

    def _read(self):
        config = ConfigParser()
        config.read(self.config_path)
        return config

    def set_value(self, section, key, value):
        config = ConfigParser()
        config.read(self.config_path)
        config.set(section, key, value)
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

        return config

    def __getitem__(self, item):
        config = self._read()
        return config[item]

    def restore_to_default(self):
        config = ConfigParser()

        config["SIMULATION"] = {
            "simulation_files_folder_path": "./Simulations/",
        }

        if not os.path.isdir(self.base_dir):
            os.makedirs(self.base_dir)

        with open(self.config_path, "w") as configfile:
            config.write(configfile)
