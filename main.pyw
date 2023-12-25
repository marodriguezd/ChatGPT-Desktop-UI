import os
import json
from threading import Thread
import PySimpleGUI as sg
import openai

CONFIG_PATH = os.path.expanduser("~")
CONFIG_FILE = os.path.join(CONFIG_PATH, 'ChatGPT-Desktop-UI_config.json')
desired_engines = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4-1106-preview']


class ChatGPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.message_history = []

    def add_message_to_history(self, role, content):
        self.message_history.append({
            "role": role,
            "content": content
        })

    def create_chat(self, engine, prompt):
        self.add_message_to_history("user", prompt)
        try:
            response = openai.ChatCompletion.create(
                model=engine,
                messages=self.message_history
            )
            chat_response = response.choices[0].message.content.strip()
            self.add_message_to_history("assistant", chat_response)
            return chat_response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


def save_config(api_key):
    with open(CONFIG_FILE, 'w') as file:
        json.dump({'api_key': api_key}, file)


def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            return config.get('api_key', '')
    return ''


def chat_window(chat_client, gpt_engines):
    sg.theme('GreenMono')
    api_key_saved = load_config()
    layout = [
        [sg.Text("Choose engine:"), sg.Combo(gpt_engines, key='-ENGINE-', default_value=gpt_engines[0], readonly=True),
         sg.Text('API Key:'), sg.InputText(api_key_saved, key='-API-KEY-', size=(30, 1))],
        [sg.Text("ChatGPT", size=(40, 1), justification='center')],
        [sg.Output(size=(80, 20), key='-OUTPUT-')],
        [sg.Multiline(size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
         sg.Button('Send', bind_return_key=True)]
    ]

    window = sg.Window("ChatGPT Interface", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Send':
            user_input = values['-QUERY-'].strip()
            if user_input:
                window['-OUTPUT-'].update(f"You: {user_input}\n\n", append=True)
                window['-QUERY-'].update('')

                chat_client.api_key = values['-API-KEY-']
                openai.api_key = chat_client.api_key
                save_config(chat_client.api_key)  # Guardar la API key

                thread = Thread(target=get_response_from_chatgpt,
                                args=(window, chat_client, values['-ENGINE-'], user_input), daemon=True)
                thread.start()
        elif event == '-CHAT_RESPONSE-':
            response = values[event]
            window['-OUTPUT-'].update(f"ChatGPT: {response}\n\n", append=True)

    window.close()


def get_response_from_chatgpt(window, chat_client, engine, prompt):
    response = chat_client.create_chat(engine, prompt)
    if response is not None:
        window.write_event_value('-CHAT_RESPONSE-', response)


def main():
    api_key = load_config() or "Enter your API key here"
    chat_client = ChatGPTClient(api_key)
    chat_window(chat_client, desired_engines)


if __name__ == "__main__":
    main()
