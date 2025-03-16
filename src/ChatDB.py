from AcroDB import AcroDB
import os

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
            self.__acrodb_ref[acrodb.get_table().table_name] = acrodb

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

    def translate_chat(self, chat: str=""):
        """
        Translate chat to FilterExpression using OpenAI.

        Boto3 Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html

        Args:
            chat (str): user-input chat in natural language
        
        Returns:
            expression (FilterExpression): OpenAI-translated FilterExpression passed into AcroDB.query()
        """

        pass
        
        '''
        prompt = """
        You are an AI that converts natural language queries into DynamoDB scan() or query() syntax.
        Rules:
        1. Use query() if the condition is on the partition key, otherwise use scan().
        2. Use boto3’s Key() for query conditions and Attr() for scan filters.
        3. Return only the Python code without explanation.

        Example inputs and outputs:

        Input: "Find all beginner parkour skills."
        Output: table.query(IndexName='status-index', KeyConditionExpression=Key('status').eq('active'))

        Input: "Get all users older than 25"
        Output: table.scan(FilterExpression=Attr('age').gt(25))

        Now convert this: "{}"
        """
        query = "Find all premium users"
        formatted_prompt = prompt.format(query)
        response = openai.responses.create(
            model="gpt-4",
            messages=[{"role": "system", "content": formatted_prompt}]
        )
        return response["choices"][0]["message"]["content"]'
        '''



def main():
    print("Script for ChatDB class.")
    print("")
    table_name: str = "Parkourpedia"
    bucket_name: str = "dsci551-acrobucket"
    acrodb_list: list[AcroDB] = [AcroDB(table_name=table_name, bucket_name=bucket_name)]

    print("TEST")
    print("-" * 50)
    print("acrodb_list:", acrodb_list)

    myChat = ChatDB(acrodb_list=acrodb_list)
    if myChat.set_api_key(API_KEY=open("secrets/API_KEY" if os.path.basename(os.getcwd()) == "AcroDB" else "../secrets/API_KEY").read()):
        print("OpenAI client setup successful!")
    
    chat = myChat.get_chat()
    FilterExpression: any = myChat.translate_chat(chat)
    print(FilterExpression)
    

if __name__ == "__main__":
    main()