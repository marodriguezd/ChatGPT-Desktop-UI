from threading import Thread

import PySimpleGUI as sg
import openai

from ConfigManager import ConfigManager
from ChatGPTClient import ChatGPTClient


class ChatWindow:
    def __init__(self, chat_client, gpt_engines, CONFIG_FILE):
        self.chat_client = chat_client
        self.CONFIG_FILE = CONFIG_FILE
        sg.theme('GreenMono')
        api_key_saved = ConfigManager.load_config(CONFIG_FILE)
        self.layout = [
            [sg.Text("Choose engine:"), sg.Combo(gpt_engines, key='-ENGINE-', default_value=gpt_engines[0], readonly=True),
             sg.Text('API Key:'), sg.InputText(api_key_saved, key='-API-KEY-', size=(30, 1))],
            [sg.Text("ChatGPT", size=(40, 1), justification='center')],
            [sg.Output(size=(80, 20), key='-OUTPUT-')],
            [sg.Multiline(size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
             sg.Button('Send', bind_return_key=True)]
        ]

    def start(self):
        window = sg.Window("ChatGPT Interface", self.layout, finalize=True)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == 'Send':
                user_input = values['-QUERY-'].strip()
                window['-OUTPUT-'].update(f"You: {user_input}\n\n", append=True)
                window['-QUERY-'].update('')

                ConfigManager.save_config(self.chat_client.api_key, self.CONFIG_FILE)  # Save the API key

                thread = Thread(target=self.get_response_from_chatgpt,
                                args=(window, values['-ENGINE-'], user_input), daemon=True)
                thread.start()

                window['-OUTPUT-'].update(f"Recibiendo respuesta...\n", append=True)

            elif event == '-CHAT_RESPONSE-':
                response = values[event]
                window['-OUTPUT-'].update(f"ChatGPT: {response}\n\n", append=True)

        window.close()

    def get_response_from_chatgpt(self, window, engine, prompt):
        response = self.chat_client.create_chat(engine, prompt)
        if response is not None:
            window.write_event_value('-CHAT_RESPONSE-', response)
