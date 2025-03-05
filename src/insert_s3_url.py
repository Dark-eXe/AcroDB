import boto3
import os
from get_value import get_value
from generate_s3_url import generate_s3_url
from insert_values import insert_value

def insert_s3_url(mvtId: str, table_name: str, bucket_name="dsci551-acrobucket"):
    os.environ["TABLE_NAME"] = table_name

    Key = f"{table_name}/mvtId-{mvtId}.png"
    Item = get_value(mvtId=mvtId)["Item"]
    URL = generate_s3_url(Bucket=bucket_name, Key=Key)

    Item["image_s3_url"] = URL
    return insert_value(event=Item, context=None, force=True)

if __name__ == "__main__":
    print("insert_s3_url")
    print("-" * 50)
    table_name = input("Enter table_name: ")
    mvtId = input("Enter mvtId: ")
    print("")
    print(insert_s3_url(mvtId=mvtId, table_name=table_name))