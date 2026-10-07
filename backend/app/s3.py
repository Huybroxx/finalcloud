import os
import boto3
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION", "ap-southeast-1"),
)


def upload_file_to_s3(file, filename: str) -> str:
    bucket = os.getenv("AWS_BUCKET_NAME", "fastapi-app-files-huynn69")
    s3_client.upload_fileobj(file, bucket, filename)
    region = os.getenv("AWS_REGION", "ap-southeast-1")
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{filename}"
    return url
