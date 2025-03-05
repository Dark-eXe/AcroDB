import boto3
import os
from botocore.exceptions import ClientError

def get_value(mvtId: str) -> dict:
    # DynamoDB client
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)

    # mvtId type check
    if not isinstance(mvtId, str):
        mvtId = str(mvtId)

    # get item
    Key = {"mvtId": mvtId}
    try:
        response = table.get_item(Key=Key)
    except ClientError as error:
        print("")
        print(error)
        print("")
        return None
    return response

if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "MAG_Code-of-Points"

    print(f"Get item from {os.environ['TABLE_NAME']}.")
    print("-" * 50)
    user_input = input("Enter mvtId: ")
    if not isinstance(user_input, str):
        user_input = str(user_input)

    print("")
    print(f"Getting mvtId {user_input} from {os.environ['TABLE_NAME']}...")
    print(get_value(mvtId=user_input))