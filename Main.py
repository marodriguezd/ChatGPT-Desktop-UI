import os.path
from ChatGPTClient import ChatGPTClient
from ChatWindow import ChatWindow
from ConfigManager import ConfigManager

CONFIG_PATH = os.path.expanduser("~")
CONFIG_FILE = os.path.join(CONFIG_PATH, 'ChatGPT-Desktop-UI-Reborn_config.json')
desired_engines = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4-1106-preview']


def main():
    api_key = ConfigManager.load_config(CONFIG_FILE) or "Enter your API Key here"
    chat_client = ChatGPTClient(api_key)
    chat_window = ChatWindow(chat_client, desired_engines, CONFIG_FILE)
    chat_window.start()


if __name__ == "__main__":
    main()
