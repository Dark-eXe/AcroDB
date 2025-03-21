import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

try:
    from src.AcroDB import AcroDB
    from src.ChatDB import ChatDB
except ModuleNotFoundError:
    module_path = os.path.abspath(os.path.join('.'))
    if module_path not in sys.path:
        sys.path.append(module_path)
    from src.AcroDB import AcroDB
    from src.ChatDB import ChatDB

def main():
    # AcroDB
    table_name, bucket_name = "MAG_Code-of-Points", "dsci551-acrobucket"
    my_acro1 = AcroDB(table_name=table_name, bucket_name=bucket_name)

    table_name, bucket_name = "Parkourpedia", "dsci551-acrobucket"
    my_acro2 = AcroDB(table_name=table_name, bucket_name=bucket_name)

    # ChatDB
    my_chat = ChatDB(acrodb_list=[my_acro1, my_acro2])
    if my_chat.set_api_key(API_KEY=open("secrets/API_KEY" if os.path.basename(os.getcwd()) == "AcroDB" else "../secrets/API_KEY").read()):
        print("OpenAI client setup successful!")
    if my_chat.set_prompt(prompt_path="src/prompts/main.txt" if os.path.basename(os.getcwd()) == "AcroDB" else "../src/prompts/main.txt"):
        print("Prompt is set!")

    my_chat.loop()

if __name__ == "__main__":
    main()