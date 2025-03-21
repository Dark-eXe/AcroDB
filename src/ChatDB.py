try:
    from .AcroDB import AcroDB
except ImportError:
    from AcroDB import AcroDB
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
from openai import OpenAI

from decimal import Decimal

class ChatDB():
    # Constructor
    ################################
    """Chat query. Interfaces with AcroDB instance(s)."""
    def __init__(self, acrodb_list: list[AcroDB]=[], API_KEY: str="", verbose: bool=False, prompt_path: str=""):
        """
        Initialize ChatDB instance.

        Args:
            acrodb_list (list[AcroDB]): AcroDB instances to interface with (can be dynamically manipulated)
            API_KEY (str): OpenAI API key (can be set later; REQUIRED for chat function, KEEP SECURE)
            verbose (bool): print OpenAI client respone
        """
        self.__acrodb_list = acrodb_list
        self.__acrodb_count = len(self.__acrodb_list)
        self.__acrodb_ref = {}
        for acrodb in self.__acrodb_list:
            self.__acrodb_ref[acrodb.get_table().table_name] = acrodb.get_table()

        self.__client = None
        if self.set_api_key(API_KEY=API_KEY) and verbose:
            print("ChatDB client successfully set.")

        self.__chat_log = []
        self.__prompt = ""
        if prompt_path:
            if not os.path.exists(prompt_path):
                prompt_path = "../" + prompt_path
            try:
                with open(prompt_path, 'r') as f:
                    self.__prompt = f.read()
            except FileNotFoundError as error:
                print(f"Prompt file not found: {error}")

    # OpenAI API Key
    ################################
    def set_api_key(self, API_KEY: str) -> bool:
        """Sets new value for API_KEY"""
        if API_KEY:
            self.__client = OpenAI(api_key=API_KEY)
            return True
        return False
    
    # OpenAI Prompt
    ################################
    def set_prompt(self, prompt_path: str="") -> bool:
        """Sets new prompt for chat with reference path."""
        try:
            with open(prompt_path, 'r') as f:
                self.__prompt = f.read()
            return True
        except FileNotFoundError as error:
            print(f"Prompt file not found: {error}")
            return False


    # Getters
    ################################
    def get_db_count(self) -> int:
        """Get count of linked AcroDB instances."""
        return self.__acrodb_count

    def get_db_list(self) -> list[AcroDB]:
        """Getter for list of linked AcroDB instances."""
        return self.__acrodb_list
    
    def get_chat_log(self) -> list[dict]:
        """Getter for chat log."""
        return self.__chat_log

    # Add/Remove from DB List
    ################################
    def add_db(self, new_db: AcroDB):
        """Add AcroDB instance to interface with."""
        self.__acrodb_list.append(new_db)
        self.__acrodb_ref[new_db.get_table().table_name] = new_db.get_table()

    def remove_db(self, db_name: str):
        """Remove AcroDB instance to interface with."""
        try:
            self.__acrodb_list.remove(self.__acrodb_ref[db_name])
        except ValueError:
            print(f"Error: {db_name} not found in linked AcroDB instances.")
            return
        try:
            del self.__acrodb_ref[db_name]
        except KeyError:
            print(f"Error: {db_name} not found in linked AcroDB instances.")
            return

    # Chat
    ################################
    def get_chat(self) -> str:
        """Get user-input query chat in natural language."""
        return str(input("Enter query: "))

    def translate_chat(self, chat: str="") -> str:
        """
        Translate NL chat to Boto3 table scan or query expression using OpenAI.

        Boto3 Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html

        Args:
            chat (str): user-input chat in natural language
        
        Returns:
            response (str): OpenAI-translated executable (or None) referencing self.__acrodb_ref
        """
        query = chat
        formatted_prompt = self.__prompt.format(query)
        sys_message = {"role": "system", "content": formatted_prompt}
        self.__chat_log.append(sys_message)

        response = self.__client.chat.completions.create(
            model="gpt-4",
            messages=self.__chat_log
        )
        assistant_response = response.choices[0].message.content
        self.__chat_log.append({"role": "assistant", "content": assistant_response})

        return assistant_response
    
    def exec_response(self, response: str="") -> any:
        """Execute chat-queried response using eval()."""
        try:
            return eval(response, {"acrodb_ref": self.__acrodb_ref, "Key": Key, "Attr": Attr, "Decimal": Decimal})
        except SyntaxError as error:
            print(f"response: {response}")
            return f"Syntax Error: {error}"
        except AttributeError as error:
            return f"Attribute Error: {error}"
        except NameError as error:
            return f"Name Error: {error}"
        except ClientError as error:
            if error.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return("Invalid data modification.")
            return f"Client Error: {error}"
        
    def print_exec_items(self, exec_response: any=None) -> None:
        """Display exec_response so that only Items are displayed in tabular form."""
        if not exec_response:
            print("No results returned.")
            return
        if not isinstance(exec_response, dict): # probably an excepted error, or table list
            print(exec_response)
            return
        if "Items" not in exec_response.keys():
            print('200: Success' if exec_response['ResponseMetadata']['HTTPStatusCode'] == 200 else "Request unsuccessful")
            return
        for Item in exec_response["Items"]:
            print(Item)

    # Pipeline
    ################################
    def loop(self):
        """Main execution loop for CLI chat-query."""
        while True:
            print("--- (q)uit to exit chat ---")
            chat = self.get_chat()
            if chat.lower() == 'q':
                break
            self.print_exec_items(self.exec_response(self.translate_chat(chat)))
            print("")



def main():
    print("Script for ChatDB class.")
    print("")
    

if __name__ == "__main__":
    main()