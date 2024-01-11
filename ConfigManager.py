import json
import os.path


class ConfigManager:
    @staticmethod
    def save_config(api_key, CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as file:
            json.dump({'api_key': api_key}, file)

    @staticmethod
    def load_config(CONFIG_FILE):
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
                return config.get('api_key', '')
        return ''
