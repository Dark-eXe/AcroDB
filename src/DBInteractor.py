import boto3
import os
import numpy as np
import pandas as pd
from decimal import Decimal
from botocore.exceptions import ClientError

class DBInteractor():
    # Constructor
    ################################
    def __init__(self, table_name: str, bucket_name: str = None):
        self.__table_name = table_name
        self.__table = boto3.resource("dynamodb").Table(table_name)
        self.__bucket = bucket_name

    # Setters & Getters
    ################################
    def get_table(self):
        return self.__table

    def get_bucket(self) -> str:
        return self.__bucket

    def set_table(self, table_name: str) -> None:
        self.__table_name = table_name
        self.__table = boto3.resource("dynamodb").Table(table_name)

    def set_bucket(self, bucket_name: str) -> None:
        self.__bucket = bucket_name

    # DB Interactions
    ################################
    def get_item(self, mvtId: str) -> dict:
        # mvtId type check
        if not isinstance(mvtId, str):
            mvtId = str(mvtId)
    
        # Invoke get_item
        Key = {"mvtId": mvtId}
        try:
            response = self.__table.get_item(Key=Key)
        except ClientError as error:
            print("")
            print(error)
            print("")
            return None
            
        return response["Item"]

    def put_item(self, Item: dict, force: bool = False):
        # Type checking -> mvtId: str, value: Decimal as supported by AWS
        if not isinstance(Item["mvtId"], str):
            Item["mvtId"] = str(Item["mvtId"])
        if not isinstance(event["value"], Decimal):
            Item["value"] = Decimal(str(Item["value"]))

        # Invoke put_item
        if force: # replaces if mvtId already exists
            self.__table.put_item(Item=Item)
        else: # no replacement if mvtId already resides in table
            try:
                self.__table.put_item(Item=Item, ConditionExpression='attribute_not_exists(mvtId)')
            except ClientError as error:
                if error.response['Error']['Code'] != 'ConditionalCheckFailedException':
                    raise

        message = f"mvtId {Item['mvtId']} successfully inserted to {self.__table_name}"
        return {"message": message}
        

    def import_xlsx(self, xlsx_path: str) -> dict:
        # Read xlsx as df
        df = pd.read_excel(xlsx_path)
        df = df.replace({np.nan: None})

        # Import values by row, invoking insert_value
        for _, row in df.iterrows():
            self.put_item(Item=dict(row))
    
        message = f"{xlsx_path} successfully imported to {self.__table_name}"
        return {"message": message}

    # S3 Bucket Media URL Interactions
    ################################
    def __generate_s3_url(self, mvtId: str, ExpiresIn: int = 604800) -> str:
        # Define parameters for generate_presigned_url
        ClientMethod = 'get_object'
        Params = {'Bucket': self.__bucket, 'Key': mvtId}

        # Invoke generate_presigned_url
        return boto3.client('s3').generate_presigned_url(
            ClientMethod=ClientMethod,
            Params=Params,
            ExpiresIn=ExpiresIn
        )

    def insert_s3_url(self, mvtId: str) -> dict:
        # Define parameters
        Key = f"{self.__table_name}/mvtId-{mvtId}.png"
        Item = self.get_item(mvtId=mvtId)

        # Generate URL
        URL = self.__generate_s3_url(Bucket=self.__bucket, Key=Key)

        # Set URL
        Item["image_s3_url"] = URL
        return self.put_item(Item=Item, force=True)

    def insert_media(self, mvtId: str, media_path: str):
        # mvtId type check
        if not isinstance(mvtId, str):
            mvtId = str(mvtId)

        # Download media from media_path
        ...

        # Upload media to S3 Bucket
        ...

        pass

    def insert_media_and_s3_url(self, mvtId: str, media_path: str):
        response_1 = self.insert_media(self, mvtId=mvtId, media_path=media_path)
        #response_2 = self.insert_s3_url(self, mvtId=mvtId)
        pass

def main():
    print("Test for AWS Client and DynamoDB table for DBInteractor instance")
    print("-" * 50)
    table_name = input("Enter DynamoDB Table name: ")
    bucket_name = input("(optional) Enter S3 Bucket name: ")
    
    myDBInteractor = DBInteractor(
        table_name=table_name, 
        bucket_name=bucket_name
    )
    test_sample = myDBInteractor.get_item(mvtId="1")
    if not test_sample:
        print("Failed. Invalid AWS Client or DynamoDB table")
        print("")
        exit()

    print("")
    print("Success! Valid AWS Client and DBInteractor instance.")
    print("")

if __name__ == "__main__":
    main()