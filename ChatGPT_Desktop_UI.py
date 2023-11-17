from threading import Thread
import PySimpleGUI as sg
import openai

desired_engines = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4-1106-preview']


def chat_window(chat_client, gpt_engines):
    sg.theme('DarkAmber')  # Color theme

    # Define layout
    layout = [
    [sg.Text("Choose engine:"), sg.Combo(gpt_engines, key='-ENGINE-', default_value=gpt_engines[0], readonly=True)],
        [sg.Text("ChatGPT", size=(40, 1), justification='center')],
        [sg.Output(size=(80, 20))],
        [sg.Multiline(size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
         sg.Button('Send', bind_return_key=True)]
    ]

    # Create Window
    window = sg.Window("ChatGPT Interface", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Send':
            user_input = values['-QUERY-'].strip()
            if user_input:
                print(f"Tú: {user_input}\n")
                window['-QUERY-'].update('')

                # Start the API call in a separate thread to prevent UI freezing
                Thread(target=get_response_from_chatgpt,
                       args=(window, chat_client, user_input)).start()
    window.close()


def get_response_from_chatgpt(window, chat_client, prompt):
    selected_engine = window['-ENGINE-'].get()  # Obtiene el motor seleccionado desde el ComboBox.
    response = chat_client.create_chat(selected_engine, prompt)  # Pasa selected_engine a create_chat.
    if response:
        print(f"ChatGPT: {response}\n")


# S: Single Responsibility Principle
class ChatGPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.message_history = []
        openai.api_key = self.api_key

    def get_engines(self):
        return openai.Engine.list()

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
            chat_response = response['choices'][0]['message']['content'].strip()
            self.add_message_to_history("assistant", chat_response)
            return chat_response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


# def wished_engines(engines):
#     gpt_engines = [engine for engine in engines if "gpt-" in engine["id"]]
#     return gpt_engines


# Main Program
def main():
    API_KEY = "YOUR_API_KEY_HERE"
    chat_client = ChatGPTClient(API_KEY)

    # Inicializar la lista de engine ids si lo necesitas aquí
    # Esto se puede hacer aquí o en otro lugar antes de llamar a chat_window
    # engines = chat_client.get_engines()["data"]
    # gpt_engines = wished_engines(engines)

    # if not gpt_engines:
    #     print("No GPT engines available.")
    #     return

    # selected_engine = gpt_engines[0]['id']
    chat_window(chat_client, desired_engines)


if __name__ == "__main__":
    main()
