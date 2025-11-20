import os
import boto3
from botocore.exceptions import ClientError

bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
print(f"Checking bucket: {bucket_name}")
print(f"Region: {os.getenv('AWS_S3_REGION_NAME')}")
print(f"Access Key ID: {os.getenv('AWS_ACCESS_KEY_ID')}")

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_S3_REGION_NAME')
)

try:
    print("Listing objects...")
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f" - {obj['Key']}")
    else:
        print("Bucket is empty.")

    print("Attempting upload...")
    s3.put_object(Bucket=bucket_name, Key='test_upload.txt', Body=b'Hello S3')
    print("Upload successful.")
except Exception as e:
    print(f"Error: {e}")
