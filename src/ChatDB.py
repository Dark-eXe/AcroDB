from AcroDB import AcroDB
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key
from openai import OpenAI

class ChatDB():
    # Constructor
    ################################
    """Chat query. Interfaces with AcroDB instance(s)."""
    def __init__(self, acrodb_list: list[AcroDB]=[], API_KEY: str="", verbose: bool=False):
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

    # OpenAI API Key
    ################################
    def set_api_key(self, API_KEY: str) -> bool:
        """Sets new value for API_KEY"""
        if API_KEY:
            self.__client = OpenAI(api_key=API_KEY)
            return True
        return False

    # Getters
    ################################
    def get_db_count(self) -> int:
        """Get count of linked AcroDB instances."""
        return self.__acrodb_count

    def get_db_list(self) -> list[AcroDB]:
        """Getter for list of linked AcroDB instances."""
        return self.__acrodb_list

    # Add/Remove from DB List
    ################################
    def add_db(self, new_db: AcroDB):
        """Add AcroDB instance to interface with."""
        self.__acrodb_list.append(new_db)
        self.__acrodb_ref[new_db.get_table().table_name] = new_db

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
        Translate chat to FilterExpression using OpenAI.

        Boto3 Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html

        Args:
            chat (str): user-input chat in natural language
        
        Returns:
            response (str): OpenAI-translated executable (or None) referencing self.__acrodb_ref
        """
        
        prompt = """
        You are an AI that converts natural language queries into DynamoDB scan() or query() syntax.
        Rules:
        1. Use query() if the condition is on the partition key, otherwise use scan().
        2. Use boto3’s Key() for query conditions and Attr() for scan filters.
        3. Return only the Python code without explanation.
        4. There are only 3 tables: Men's Artistic Gymnastics Code of Points (or MAG), Women's Artistic Gymnastics Code of Points (or WAG), Parkour dictionary (or Parkourpedia)
        5. DynamoDB tables should only be referenced with the syntax: self.__acrodb_ref[<table_name>]
        6. Only possible values for <table_name> are "MAG_Code-of-Points", "WAG_Code-of-Points", "Parkourpedia"
        7. "mvtId" or movement ID is the only partition key among all tables, current syntax is integers wrapped in string
        8. Current "mvtId" range for MAG is [1, 204], for WAG is none, for Parkour is [1, 12]
        9. In gymnastics, difficulty 'A' or value '0.1' is easy, difficulty 'B' or value '0.2' is intermediate, difficulty 'C' or value '0.3' is difficult, and so on until difficulty 'J' or value '1.0' being the most difficult and rarest
        10. Attributes in "Parkourpedia": 'group', 'name', 'difficulty', 'description', 'image_s3_url'
        11. 'group' value possibilites in "Parkourpedia": 'Wall', 'Vault', 'Landing', 'Bar', 'Flip'
        12. 'difficult' value possibilities in "Parkourpedia": 'Situational', 'Beginner', 'Intermediate', 'Advanced'
        13. Attributes in MAG/WAG: 'difficulty', 'event', 'group', 'name', 'value', 'image_s3_url'
        14. 'event' value possibilities in MAG: 'MAG Floor', 'MAG Pommel Horse', 'MAG Rings'
        15. Output None for non-possibilities.
        
        Example inputs and outputs:

        Input: "Find all beginner parkour skills."
        Output: self.__acrodb_ref["Parkourpedia"].scan(FilterExpression=Attr('age').gt(25))

        Input: "Get me skill ID 1 from the Men's Gymnastics table."
        Output: self.__acrodb_ref["MAG_Code-of-Points"].query(KeyConditionExpression=Key('mvtId').eq('1'))

        Input: "Show me difficult floor skills in Men's Gymnastics."
        Output: self.__acrodb_ref["MAG_Code-of-Points"].scan(FilterExpression=Attr('difficulty').gte('C'))

        Input: "Show me some Women's Gymnastics skills."
        Output: None

        Input: "Find movement 50 in parkour."
        Output: None

        Input: "What are some parkour wall skill names."
        Output: self.__acrodb_ref["Parkourpedia"].scan(FilterExpression=Attr('group').eq('Wall'), ProjectionExpression="name")

        Now convert this: "{}"
        """
        query = chat
        formatted_prompt = prompt.format(query)  # Fix string formatting

        response = self.__client.chat.completions.create(  # Corrected API call
            model="gpt-4",
            messages=[{"role": "system", "content": formatted_prompt}]
        )

        return response.choices[0].message.content



def main():
    print("Script for ChatDB class.")
    print("")
    table_name: str = "Parkourpedia"
    bucket_name: str = "dsci551-acrobucket"
    acrodb_list: list[AcroDB] = [AcroDB(table_name=table_name, bucket_name=bucket_name)]

    print("TEST")
    print("-" * 50)
    myChat = ChatDB(acrodb_list=acrodb_list)
    print("Parkourpedia added!")
    myChat.add_db(AcroDB(table_name="MAG_Code-of-Points", bucket_name="dsci551-acrobucket"))
    print("MAG_Code-of-Points added!")
    if myChat.set_api_key(API_KEY=open("secrets/API_KEY" if os.path.basename(os.getcwd()) == "AcroDB" else "../secrets/API_KEY").read()):
        print("OpenAI client setup successful!")
    
    print("")
    chat = myChat.get_chat()
    print("")
    print("RESPONSE")
    print("-" * 25)
    response = myChat.translate_chat(chat)
    print(response)
    print("")
    

if __name__ == "__main__":
    main()