from AcroDB import AcroDB

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
        return str(input("Enter query: "))

    # Translate chat to FilterExpression using OpenAI
    def translate_chat(self, chat: str=""):
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
    print("Your chat:", chat)

if __name__ == "__main__":
    main()