import boto3
import os

def generate_s3_url(Bucket: str, Key: str) -> str:
    ClientMethod = 'get_object'
    Params = {'Bucket': Bucket, 'Key': Key}
    ExpiresIn = 604800

    return boto3.client('s3').generate_presigned_url(
        ClientMethod=ClientMethod,
        Params=Params,
        ExpiresIn = 604800
    )

if __name__ == "__main__":
    Bucket = input("Enter bucket: ")
    Key = input("Enter key: ")
    print("")
    print("URL")
    print("-" * 50)
    print(generate_s3_url(Bucket=Bucket, Key=Key))
    print("")