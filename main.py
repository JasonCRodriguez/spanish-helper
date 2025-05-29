import json
from ollama import chat, Client
from ollama._types import ResponseError as ollamaResponseError
import logging
import random
from wordfreq import top_n_list

from instructions import get_instructions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SpanishHelper():

    MODEL_NAME = "qwen3"

    def __init__(self):

        self.initialize_model()

    def initialize_model(self):
        """
        Initialize the Ollama model.
        This function is a placeholder for any model initialization logic.
        """
        try:
            # Check if the model is already loaded
            chat(self.MODEL_NAME, [{"role": "system",
                                    "content": "Eres un tutor de español. Ayuda al usuario a aprender español. Solamente usa español."}])
            logging.info(f"Model '{self.MODEL_NAME}' is already loaded.")
        except ollamaResponseError as e:
            client = Client()
            client.pull(self.MODEL_NAME)
            logging.info(f"Model '{self.MODEL_NAME}' pulled successfully.")
        
        logging.info("Model initialized successfully.")
    
    def base_loop(self, messages=None, mode=''):
        """
        Base loop for the Spanish helper.
        This function is a placeholder for any base loop logic.
        """
        response = chat(
                self.MODEL_NAME,
                messages=[*messages]
            )
        while True:
            print(response.message.content + '\n')
            user_input = input('<{}>: '.format(mode))
            response = chat(
                self.MODEL_NAME,
                messages=[*messages, {'role': 'user', 'content': user_input}],
            )

            # Add the response to the messages to maintain the history
            messages += [
                {'role': 'user', 'content': user_input},
                {'role': 'assistant', 'content': response.message.content},
            ]
    
    def word_quiz(self):
        print("\n[Word Quiz]")
        message = [{"role": "system", "content": get_instructions('word')}]
        self.base_loop(messages=message, mode='word')

    def sentence_quiz(self):
        print("\n[Sentence Quiz]")

        message = [{"role": "system", "content": get_instructions('sentence')},]
        self.base_loop(messages=message, mode='sentence')

    def role_play(self):
        print("\n[Role-Play]")
        
        messages = [{"role": "system", "content": get_instructions('role-play')}]
        self.base_loop(messages=messages, mode='role-play')
        
    def story_building(self):
        print("\n[Story Building]")
        messages = [{"role": "system", "content": get_instructions('story')}]
        self.base_loop(messages=messages, mode='story')

    def main(self):
        while True:
            print("\n--- Spanish Helper ---")
            print("1. Word Quiz")
            print("2. Sentence Quiz")
            print("3. Role-Play")
            print("4. Story Building")
            print("5. Salir")
            choice = input("Selecciona un modo de juego (1-5): ")
            if choice == "1":
                self.word_quiz()
            elif choice == "2":
                self.sentence_quiz()
            elif choice == "3":
                self.role_play()
            elif choice == "4":
                self.story_building()
            elif choice == "5":
                print("¡Hasta luego!")

                break
            else:
                print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    spanish_helper = SpanishHelper()
    spanish_helper.main()
