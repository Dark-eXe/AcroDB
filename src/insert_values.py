import boto3
from decimal import Decimal
import os
from botocore.exceptions import ClientError

def insert_value(event: any, context: any, force=False):
    
    # DynamoDB client
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)
    
    # Insert value
    if not isinstance(event["mvtId"], str):
        event["mvtId"] = str(event["mvtId"])
    if not isinstance(event["value"], Decimal):
        event["value"] = Decimal(str(event["value"]))
    if force: # replaces if mvtId already exists
        table.put_item(Item=event)
    else:
        try:
            table.put_item(Item=event, ConditionExpression='attribute_not_exists(mvtId)')
        except ClientError as error:
            if error.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise

    # Return message
    message = f"mvtId {event['mvtId']} successfully inserted to {table_name}"
    return {"message": message}

if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "MAG_Code-of-Points"
    test_event = {"mvtId": "2", "difficulty": "A", "event": "MAG Floor", "group": "Non-acrobatic Elements", "image_s3_url": None, "name": "From hdst. lower to L-sit or strad. L-sit (2 s.)", "value": 0.1}
    
    print("Testing insert_values")
    print("-" * 50)
    print(f"Table: \t{os.environ['TABLE_NAME']}")
    print(f"Event: \t{test_event}")
    print("")
    
    print(insert_value(event=test_event, context=None))