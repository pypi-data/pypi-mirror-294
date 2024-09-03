import yaml
import os
import logging
from logging.handlers import RotatingFileHandler

class Config:
    def __init__(self, default_config_path='src/config/default_config.yaml', config_path='src/config/config.yaml'):
        self.default_config_path = default_config_path
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        # Charger la configuration par défaut
        if not os.path.exists(self.default_config_path):
            raise FileNotFoundError(f"Default configuration file '{self.default_config_path}' not found.")
        with open(self.default_config_path, 'r') as default_config_file:
            default_config = yaml.safe_load(default_config_file)
        
        # Charger la configuration spécifique à l'environnement, si elle existe
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                config = yaml.safe_load(config_file)
            self.merge_configs(default_config, config)
        
        return default_config

    def merge_configs(self, default, custom):
        if custom is None:
            return  # Exit the function if custom is None
        for key, value in custom.items():
            if isinstance(value, dict) and key in default:
                self.merge_configs(default[key], value)
            else:
                default[key] = value

    def get(self, section, key, default=None):
        return self.config_data.get(section, {}).get(key, default)
    
    def set(self, section, key, value):
        if section not in self.config_data:
            self.config_data[section] = {}
        self.config_data[section][key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_path, 'w') as config_file:
            yaml.safe_dump(self.config_data, config_file)

    def configure_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        log_to_file = self.get('logging', 'log_to_file')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        if log_to_file:
            logger.addHandler(file_handler)
        else:
            logger.addHandler(console_handler)

        return logger
# Exemple d'utilisation:
# config = Config()
# SERVER_HOST = config.get('server', 'host')
# SERVER_PORT = config.get('server', 'port')
# UPLOAD_FOLDER = config.get('general', 'upload_folder')
