import openai


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

# El resto de la clase UserInterface se mantiene igual

# El resto del código principal se mantiene igual