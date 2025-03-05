import boto3
import os
from get_value import get_value
from generate_s3_url import generate_s3_url
from insert_values import insert_value

def insert_s3_url(mvtId: str, table_name="dsci551_acroDB", bucket_name="dsci551-acrobucket"):
    os.environ["TABLE_NAME"] = table_name
    
    Item = get_value(mvtId=mvtId)["Item"]
    URL = generate_s3_url(Bucket=bucket_name, Key=f"mvtId-{mvtId}.png")

    Item["image_s3_url"] = URL
    return insert_value(event=Item, context=None, force=True)

if __name__ == "__main__":
    mvtId = input("Enter mvtId: ")
    print(insert_s3_url(mvtId=mvtId))