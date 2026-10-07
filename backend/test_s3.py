import io
import json
import boto3
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

print("==================================================")
print("        TESTING AWS S3 FILE UPLOAD ENDPOINT       ")
print("==================================================")
print(f"Bucket Name: {settings.AWS_BUCKET_NAME}")
print(f"AWS Region:  {settings.AWS_REGION}")
print("Endpoint:    POST /upload")

client = TestClient(app)

# 1. Test live upload via endpoint
test_data = b"Proof of successful upload to AWS S3 via FastAPI endpoint!"
test_filename = "proof-task3-upload.txt"

print(f"\nUploading file '{test_filename}' via FastAPI...")
response = client.post(
    "/upload",
    files={"file": (test_filename, io.BytesIO(test_data), "text/plain")}
)

if response.status_code == 200:
    data = response.json()
    print("\n[SUCCESS] Successful file upload to S3!")
    print(f"Status Code:   {response.status_code} OK")
    print(f"File Name:     {data.get('filename')}")
    print(f"S3 Object URL: {data.get('url')}")
    
    # 2. Check S3 bucket directly
    s3 = boto3.client("s3", region_name=settings.AWS_REGION)
    objs = s3.list_objects_v2(Bucket=settings.AWS_BUCKET_NAME)
    print("\nCurrent Files in S3 Bucket:")
    for item in objs.get("Contents", []):
        print(f"  - {item['Key']} ({item['Size']} bytes)")
    print("==================================================")
else:
    print(f"\n[FAILED] Upload error: {response.text}")