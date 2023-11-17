import openai


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
            # response = openai.Completion.create(engine=engine, prompt=prompt)
            chat_response = response['choices'][0]['message']['content'].strip()
            self.add_message_to_history("assistant", chat_response)
            return chat_response
            # return response['choices'][0]['message']['content'].strip()
            # return response.choices[0].text.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


# O: Open/Closed Principle
class UserInterface:
    def display_engines(self, engines):
        # Define el orden deseado
        desired_engines = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4-1106-preview"]

        # Filtra y ordena los motores
        filtered_ordered_engines = [engine for engine_id in desired_engines for engine in engines if
                                    engine['id'] == engine_id]

        print("\nVersiones GPT específicas:")
        for i, engine in enumerate(filtered_ordered_engines, start=1):
            print(f"{i}. {engine['id']}")

        return filtered_ordered_engines

    '''def display_engines(self, engines):
        gpt_engines = [engine for engine in engines if "gpt-" in engine["id"]]
        print("Available ChatGPT versions:")
        for i in range(len(gpt_engines)):
            print(f"{i+1}. {gpt_engines[i]['id']}")
        """for i, engine in enumerate(engines, start=1):
            print(f"{i}. {engine['id']}")"""
        return gpt_engines'''

    def select_engine(self, engines):
        choice = int(input("Selecciona la versión de ChatGPT (por número): "))
        return engines[choice - 1]["id"]

    def get_prompt(self):
        return input("\n¿Qué te gustaría preguntar a ChatGPT?: ")


# Main Program
def main():
    API_KEY = "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"

    chat_client = ChatGPTClient(API_KEY)
    ui = UserInterface()

    engines = chat_client.get_engines()["data"]
    gpt_engines = ui.display_engines(engines)
    if not gpt_engines:
        print("No GPT engines available.")
        return

    selected_engine = ui.select_engine(gpt_engines)

    while True:
        prompt = ui.get_prompt()

        print("Recibiendo respuesta...")

        response = chat_client.create_chat(selected_engine, prompt)

        if response:
            print(f"\nChatGPT responde: {response}")
        else:
            print("Failed to get a response from ChatGPT.")


if __name__ == "__main__":
    main()
