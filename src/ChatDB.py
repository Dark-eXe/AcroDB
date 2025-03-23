try:
    from .AcroDB import AcroDB
except ImportError:
    from AcroDB import AcroDB
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
from openai import OpenAI, RateLimitError

from decimal import Decimal
import itertools

class ChatDB():
    # Constructor
    ################################
    """Chat query. Interfaces with AcroDB instance(s)."""
    def __init__(self, acrodb_list: list[AcroDB]=[], API_KEY: str="", prompt_path: str="", verbose: bool=False):
        """
        Initialize ChatDB instance.

        Args:
            acrodb_list (list[AcroDB]): AcroDB instances to interface with (can be set/reset later)
            API_KEY (str): OpenAI API key (can be set/reset later; REQUIRED for chat function, KEEP SECURE)
            prompt_path (str): path to OpenAI prompt (can be set/reset later)
            verbose (bool): print OpenAI client response
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

        try:
            response = self.__client.chat.completions.create(
                model="gpt-4",
                messages=self.__chat_log[-3:] if len(self.__chat_log) > 3 else self.__chat_log
            )
        except RateLimitError as error:
            print(f"Rate Limit Error: {error}")
            return None
        
        assistant_response = response.choices[0].message.content
        self.__chat_log.append({"role": "assistant", "content": assistant_response})

        return assistant_response
    
    def exec_response(self, response: str="") -> any:
        """Execute chat-queried response using eval()."""
        try:
            return eval(response, {"acrodb_ref": self.__acrodb_ref, "Key": Key, "Attr": Attr, "Decimal": Decimal, "boto3": boto3, "itertools": itertools})
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
        
    def exec_items(self, exec_response: any=None) -> str:
        """Display exec_response so that Items are displayed in tabular form."""
        if not exec_response:
            return "No results returned."
        if not isinstance(exec_response, dict):  # Probably an error message or a plain list of tables
            return str(exec_response)

        if "Items" in exec_response:
            items_output = [str(item) for item in exec_response["Items"]]
            return items_output if items_output else "No matching items found."

        if "Table" in exec_response:  # For describe_table()
            table_info = "\nTABLE DETAILS\n" + "-" * 15 + "\n"
            table_info += "\n".join([f"{key}: {value}" for key, value in exec_response["Table"].items()])
            return table_info

        if "Count" in exec_response:  # For count queries
            return f"Total count: {exec_response['Count']}"

        if "ResponseMetadata" in exec_response:
            status_code = exec_response["ResponseMetadata"].get("HTTPStatusCode", 400)
            return "200: Success" if status_code == 200 else f"Request unsuccessful (Status: {status_code})"
        
        # Fallback case for unknown structures
        return str(exec_response)


    # CLI Pipeline
    ################################
    def loop(self):
        """Main execution loop for CLI chat-query."""
        while True:
            print("--- (q)uit to exit chat ---")
            chat = self.get_chat()
            if chat.lower() == 'q':
                break
            print(self.exec_items(self.exec_response(self.translate_chat(chat))))
            print("")



def main():
    print("Script for ChatDB class.")
    print("")
    

if __name__ == "__main__":
    main()