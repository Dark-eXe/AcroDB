import boto3
import os
import numpy as np
import pandas as pd
from decimal import Decimal
from botocore.exceptions import ClientError

class AcroDB():
    """Interface with AcroDB database AWS DynamoDB table and linked S3 multimedia bucket."""
    # Constructor
    ################################
    def __init__(self, table_name: str, bucket_name: str=None):
        """
        Initialize AcroDB instance.

        Args:
            table_name (str): DynamoDB table name (required, can be dynamically replaced)
            bucket_name (str): S3 bucket name (default None, can be dynamically replaced)
        """
        self.__table_name = table_name
        self.__table = boto3.resource("dynamodb").Table(table_name)
        self.__bucket = bucket_name
        self.__s3_client = boto3.client('s3')

    # Setters & Getters
    ################################
    def get_table(self):
        """Getter for DynamoDB table as boto3 resource."""
        return self.__table

    def get_bucket(self) -> str:
        """Getter for S3 bucket as bucket name."""
        return self.__bucket

    def set_table(self, table_name: str) -> None:
        """Setter for DynamoDB table."""
        self.__table_name = table_name
        self.__table = boto3.resource("dynamodb").Table(table_name)

    def set_bucket(self, bucket_name: str) -> None:
        """Setter for S3 bucket."""
        self.__bucket = bucket_name

    # DB Interactions
    ################################
    def get_item(self, mvtId: str) -> dict:
        """
        Gets item from DynamoDB table.

        Args:
            mvtId (str): primary key

        Returns:
            response["Item"] (dict): query return item from boto3
        """
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

    def put_item(self, Item: dict, force: bool=False) -> dict:
        """
        Puts item in DynamoDB table.
        
        Args:
            Item (dict): JSON to put in table (MUST have "mvtId" primary key)
            force (bool): replace existing item in table if True (default False)
        
        Returns:
            message (dict): JSON response message
        """
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
        """
        Imports entries from xlsx workbork into DynamoDB table.
        
        Args:
            xlsx_path (str): path to xlsx workbook (with entries having "mvtId" primary key)
            
        Returns:
            message (dict): JSON response message
        """
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
        """Calls s3_client.generate_presigned_url()"""
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
        """Generates and puts S3 url into corresponding Item in DynamoDB table."""
        # Define parameters
        Key = f"{self.__table_name}/mvtId-{mvtId}{ext}"
        Item = self.get_item(mvtId=mvtId)

        # Generate URL
        URL = self.__generate_s3_url(Bucket=self.__bucket, Key=Key)

        # Set URL
        Item["image_s3_url"] = URL
        return self.put_item(Item=Item, force=True)

    def __insert_media(self, mvtId: str, media_path: str) -> bool:
        """Uploads local multimedia into S3 multimedia bucket."""
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

    def insert_media_and_s3_url(self, mvtId: str, media_path: str) -> dict:
        """
        Uploads local multimedia into S3 bucket and corresponding Item in DynamoDB table.
        
        Args:
            mvtId (str): primary key
            media_path (str): path to multimedia
            
        Returns:
            response: JSON response message"""
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
            FilterExpression="",):
        """
        Direct query to DynamoDB table using boto3 scan() method.
        
        Args:
            IndexName (str): GSI for table (NOT YET SUPPORTED)
            Limit (int): query search limit (default 100)
            Select (str): for filter use with GSI (NOT YET SUPPORTED)
            FilterExpression (FilterExpression): boto3 query expression"""
        if IndexName:
            print("Query: IndexName not yet supported.")

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
        """Returns file extension of given filename."""
        # Extracts the file extension using os.path.splitext
        _, extension = os.path.splitext(filename)
        return extension

def main():
    print("Script for AcroDB class.")
    print("")

if __name__ == "__main__":
    main()