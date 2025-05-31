import json
from ollama import chat, Client
from ollama._types import ResponseError as ollamaResponseError
import logging
import random
from wordfreq import top_n_list
from collections import Counter

from instructions import get_instructions

from rich.console import Console
from rich.markdown import Markdown

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SpanishHelper():

    MODEL_NAME = "qwen3"

    def __init__(self):

        self.console = Console()
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
        self.database = self.get_or_setup_database()

    def get_or_setup_database(self):
        """
        Get or setup the database for the Spanish helper.
        This function is a placeholder for any database setup logic.
        """
        try:
            with open('database.json', 'r') as file:
                data = json.load(file)
                logging.info("Database loaded successfully.")
                return data
        except FileNotFoundError:
            logging.warning("Database not found. Setting up a new database.")
            top_n_es_list = [word for word in top_n_list('es', 1000) if word.isalpha() and len(word) > 1]
            top_n_en_list = [word for word in top_n_list('en', 1000) if word.isalpha() and len(word) > 1]
            top_n_list_comb = top_n_es_list + top_n_en_list
            data = {
                "word_list": top_n_list_comb,
                "words_correct_counter": {},
                "tiempos_verbales": [
                    "presente", "pretérito perfecto", "imperfecto", "futuro simple",
                    "condicional simple", "pretérito imperfecto", "pretérito pluscuamperfecto",
                    "futuro perfecto", "condicional perfecto", "presente subjuntivo",
                    "imperfecto subjuntivo", "pretérito perfecto subjuntivo", "futuro subjuntivo"
                ],
                "sentence_correct_counter": {},
            }
            return data
    
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
            self.console.print(Markdown(response.message.content + '\n'))
            user_input = input('<{}> (type "exit" to return): '.format(mode))
            if user_input.strip().lower() == "exit":
                self.console.print("[bold yellow]Saliendo al menú principal...[/bold yellow]\n")
                break
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
    
    def reading_comprehension(self):
        print("\n[Reading Comprehension]")
        messages = [{"role": "system", "content": get_instructions('reading_comprehension')}]
        self.base_loop(messages=messages, mode='reading_comprehension')

    def main(self):
        while True:
            print("\n--- Spanish Helper ---")
            print("1. Word Quiz")
            print("2. Sentence Quiz")
            print("3. Role-Play")
            print("4. Story Building")
            print("5. Reading Comprehension")
            print("6. Salir")
            choice = input("Selecciona un modo de juego (1-6): ")
            if choice == "1":
                self.word_quiz()
            elif choice == "2":
                self.sentence_quiz()
            elif choice == "3":
                self.role_play()
            elif choice == "4":
                self.story_building()
            elif choice == "5":
                self.reading_comprehension()
            elif choice == "6":
                print("¡Hasta luego!")

                break
            else:
                print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    spanish_helper = SpanishHelper()
    spanish_helper.main()
