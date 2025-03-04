import boto3
from decimal import Decimal
import os

def insert_value(event: any, context: any):
    
    # DynamoDB client
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)
    
    # Insert value
    if not isinstance(event["mvtId"], str):
        event["mvtId"] = str(event["mvtId"])
    if not isinstance(event["value"], Decimal):
        event["value"] = Decimal(str(event["value"]))
    table.put_item(Item=event)

    # Return message
    message = f"mvtId {event['mvtId']} successfully inserted to {table_name}"
    return {"message": message}

if __name__ == "__main__":
    print("Testing insert_values"
    
    os.environ["TABLE_NAME"] = "dsci551_acroDB"
    test_event = {"mvtId": "2", "difficulty": "A", "event": "MAG Floor", "group": "Non-acrobatic Elements", "image_s3_url": None, "name": "From hdst. lower to L-sit or strad. L-sit (2 s.)", "value": 0.1}

    print(insert_value(event=test_event, context=None))