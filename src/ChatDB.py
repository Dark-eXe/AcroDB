from src import AcroDB
import boto3
import os
import numpy as np
import pandas as pd
from decimal import Decimal
from botocore.exceptions import ClientError

import openai

class ChatDB():
    # Constructor
    ################################
    def __init__(self, acrodb_list: list[AcroDB]=[]):
        self.__acrodb_list = acrodb_list
        self.__acrodb_count = len(self.__acrodb_list)

    # Getters
    ################################
    def get_db_count(self) -> int:
        return self.__acrodb_count

    def get_db_list(self) -> list[AcroDB]:
        return self.__acrodb_list

    # Add/Remove from DB List
    ################################
    def add_db(self, new_db: AcroDB):
        self.__acrodb_list.append(new_db)

    def remove_db(self, db: AcroDB):
        self.__acrodb_list.remove(db)

    # Chat
    ################################
    def get_chat(self) -> str:
        pass

    # Translate chat to FilterExpression using OpenAI
    def translate_chat(self, chat: str=""):
        pass

def main():
    print("Script for ChatDB class.")
    print("")

if __name__ == "__main__":
    main()