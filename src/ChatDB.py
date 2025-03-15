from AcroDB import AcroDB

import openai

class ChatDB():
    # Constructor
    ################################
    """Chat query. Interfaces with AcroDB instance(s)."""
    def __init__(self, acrodb_list: list[AcroDB]=[]):
        """
        Initialize ChatDB instance.

        Args:
            acrodb_list (list[AcroDB]): AcroDB instances to interface with (default empty, can be dynamically manipulated)
        """
        self.__acrodb_list = acrodb_list
        self.__acrodb_count = len(self.__acrodb_list)

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

    def remove_db(self, db: AcroDB):
        """Remove AcroDB instance to interface with."""
        self.__acrodb_list.remove(db)

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

def main():
    print("Script for ChatDB class.")
    print("")
    table_name: str = "MAG_Code-of-Points"
    bucket_name: str = "dsci551-acrobucket"
    acrodb_list: list[AcroDB] = [AcroDB(table_name=table_name, bucket_name=bucket_name)]
    print("TEST")
    print("-" * 50)
    print("acrodb_list:", acrodb_list)
    myChat = ChatDB(acrodb_list=acrodb_list)
    chat = myChat.get_chat()
    FilterExpression: any = myChat.translate_chat(chat)
    

if __name__ == "__main__":
    main()