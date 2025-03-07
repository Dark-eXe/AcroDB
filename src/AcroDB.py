import boto3
import os
import numpy as np
import pandas as pd
from decimal import Decimal
from botocore.exceptions import ClientError

class AcroDB():
    # Constructor
    ################################
    def __init__(self, table_name: str, bucket_name: str=None):
        self.__table_name = table_name
        self.__table = boto3.resource("dynamodb").Table(table_name)
        self.__bucket = bucket_name
        self.__s3_client = boto3.client('s3')

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

    def put_item(self, Item: dict, force: bool=False):
        # Type checking -> mvtId: str, value: Decimal as supported by AWS
        if not isinstance(Item["mvtId"], str):
            Item["mvtId"] = str(Item["mvtId"])
        if not isinstance(Item["value"], Decimal):
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
    def __generate_s3_url(self, Bucket: str, Key: str, ExpiresIn: int=604800) -> str:
        # Define parameters for generate_presigned_url
        ClientMethod = 'get_object'
        Params = {'Bucket': self.__bucket, 'Key': Key}

        # Invoke generate_presigned_url
        return self.__s3_client.generate_presigned_url(
            ClientMethod=ClientMethod,
            Params=Params,
            ExpiresIn=ExpiresIn
        )

    def __insert_s3_url(self, mvtId: str, ext: str) -> dict:
        # Define parameters
        Key = f"{self.__table_name}/mvtId-{mvtId}{ext}"
        Item = self.get_item(mvtId=mvtId)

        # Generate URL
        URL = self.__generate_s3_url(Bucket=self.__bucket, Key=Key)

        # Set URL
        Item["image_s3_url"] = URL
        return self.put_item(Item=Item, force=True)

    def __insert_media(self, mvtId: str, media_path: str) -> bool:
        # mvtId type check
        if not isinstance(mvtId, str):
            mvtId = str(mvtId)

        # media_path check
        if not os.path.exists(media_path):
            print(f"'{media_path}' does not exist.")
            return False

        # Get extension
        ext = self.__get_file_extension(media_path)

        # Upload media to S3 Bucket
        try:
            self.__s3_client.upload_file(
                Filename=media_path, 
                Bucket=self.__bucket, 
                Key=f"{self.__table.table_name}/mvtId-{mvtId}{ext}"
                )
        except ClientError as e:
            print(e)
            return False
        return True

    def insert_media_and_s3_url(self, mvtId: str, media_path: str):
        response_1 = self.__insert_media(mvtId=mvtId, media_path=media_path)
        if not response_1:
            return None
        ext = self.__get_file_extension(media_path)
        response_2 = self.__insert_s3_url(mvtId=mvtId, ext=ext)
        return response_2

    # Query
    ################################
    def query(
        self,
        IndexName: str="", Limit: int=100, Select: str="ALL_ATTRIBUTES",
        ProjectionExpression: str="", FilterExpression="",
        ExpressionAttributeNames: dict={}, ExpressionAttributeValues: dict={}
    ):
        if IndexName:
            print("Query: IndexName not yet supported.")
        if ProjectionExpression:
            print("Query: ProjectionExpression not yet supported.")
        if ExpressionAttributeNames:
            print("Query: ExpressionAttributeNames not yet supported.")
        if ExpressionAttributeValues:
            print("Query: ExpressionAttributeValues not yet supported.")

        if FilterExpression:
            return self.__table.scan(
                Limit=Limit,
                FilterExpression=FilterExpression
        )
        
        return self.__table.scan(
            Limit=Limit
        )
        

    # Miscellaneous
    ################################
    def __get_file_extension(self, filename):
        # Extracts the file extension using os.path.splitext
        _, extension = os.path.splitext(filename)
        return extension

def main():
    print("Script for AcroDB class.")
    print("")

if __name__ == "__main__":
    main()