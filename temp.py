import PySimpleGUI as sg
from threading import Thread


def chat_window(chat_client):
    sg.theme('DarkAmber')  # Color theme

    # Define layout
    layout = [
        [sg.Text("ChatGPT", size=(40, 1), justification='center')],
        [sg.Output(size=(80, 20))],
        [sg.Multiline(size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
         sg.Button('Send', bind_return_key=True)]
    ]

    # Create window
    window = sg.Window("ChatGPT Interface", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Send':
            user_input = values['-QUERY-'].strip()
            if user_input:
                print(f"You: {user_input}")
                window['-QUERY-'].update('')

                # Start the API call in a separate thread to prevent UI freezing
                Thread(target=get_response_from_chatgpt,
                       args=(window, chat_client, user_input, selected_engine)).start()

    window.close()


def get_response_from_chatgpt(window, chat_client, prompt, engine):
    response = chat_client.create_chat(engine, prompt)
    if response:
        print(f"ChatGPT: {response}")


# Then modify the main program to use PySimpleGUI
def main():
    # ... existing code ...
    chat_window(chat_client)

# ... existing code ...