import boto3
import os
from get_value import get_value

def insert_media(mvtId: str, media_path: str):
    # DynamoDB client
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)

    # mvtId type check
    if not isinstance(mvtId, str):
        mvtId = str(mvtId)

    pass

if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "MAG_Code-of-Points"

    print(f"Insert media into {os.environ['TABLE_NAME']}.")
    print("-" * 50)
    user_input = input("Enter mvtId: ")
    if not isinstance(user_input, str):
        user_input = str(user_input)

    print("")
    print(f"Getting mvtId {user_input} from {os.environ['TABLE_NAME']}...")
    response = get_value(mvtId=user_input)
    if not response:
        print(f"Error retrieving item from {os.environ['TABLE_NAME']}")
        exit()
    if "Item" not in response.keys():
        print(f"mvtId {user_input} not found in {os.environ['TABLE_NAME']}")
    