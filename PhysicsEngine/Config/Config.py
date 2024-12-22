from configparser import ConfigParser
import os

class Config:
    """
    Class for handling config (creating default, reading and writing)

    Config file (config.ini) will be created on first use of this class in the root directory of the project.
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.abspath(os.path.join(__file__, "..", "..", "..", "config.ini"))

        if not os.path.isfile(self.config_path):
            self.restore_to_default()

    def _read(self):
        """
        Reads the config file

        Returns:
            ConfigParser: ConfigParser object
        """
        config = ConfigParser()
        config.read(self.config_path)
        return config

    def set_value(self, section: str, key: str, value: str) -> str:
        """
        Sets the value in the config file
        Args:
            section (string): section from the config file
            key (string): key of the config setting
            value (string): value to set the key in section to

        Returns:
            ConfigParser: ConfigParser object

        """
        config = ConfigParser()
        config.read(self.config_path)
        config.set(section, key, value)
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

        return config

    def __getitem__(self, item: str) -> str:
        """
        Get the value of the item from the config file

        Use double brackets to specify section and key

        Args:
            item (string): section or key from the config file

        Returns:
            string: value of the item

        Examples:
            config["Section"]["Key"]
        """
        config = self._read()
        return config[item]

    def restore_to_default(self):
        """
        Restores config file to default

        Returns:
            None
        """
        config = ConfigParser()

        config["SIMULATION"] = {
            "simulation_files_folder_path": "./Simulations/",
        }

        if not os.path.isdir(self.base_dir):
            os.makedirs(self.base_dir)

        with open(self.config_path, "w") as configfile:
            config.write(configfile)
