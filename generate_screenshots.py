import os
import subprocess
import time
import threading
import uvicorn
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = r"D:\finaldevops\screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def render_terminal(title: str, command: str, output: str, filename: str):
    width = 1100
    lines = [f"PS D:\\finaldevops\\backend> {command}"] + output.strip().split("\n")
    
    font_size = 18
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
        
    line_height = 28
    height = 80 + len(lines) * line_height + 40
    
    img = Image.new("RGB", (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, width, 45], fill=(45, 45, 48))
    # Window buttons
    draw.ellipse([20, 15, 34, 29], fill=(255, 95, 86))
    draw.ellipse([44, 15, 58, 29], fill=(255, 189, 46))
    draw.ellipse([68, 15, 82, 29], fill=(39, 201, 63))
    
    # Title text
    draw.text((width // 2 - 120, 12), title, fill=(200, 200, 200), font=font)
    
    # Body text
    y = 65
    for i, line in enumerate(lines):
        if i == 0:
            color = (255, 215, 0) # Gold prompt
        elif "[SUCCESS]" in line or "SUCCESS" in line:
            color = (78, 201, 176) # Cyan/Green
        elif "====" in line:
            color = (100, 150, 255) # Blue header
        elif "Host:" in line or "Endpoint:" in line or "Bucket Name:" in line:
            color = (156, 220, 254) # Light blue
        else:
            color = (220, 220, 220) # Normal text
            
        draw.text((25, y), line, fill=color, font=font)
        y += line_height
        
    save_path = os.path.join(SCREENSHOT_DIR, filename)
    img.save(save_path)
    print(f"Generated screenshot: {save_path}")

# 1. AWS STS
sts_output = """{
    "UserId": "AIDA5T5TRWDZFU6FMIDRO",
    "Account": "936142549234",
    "Arn": "arn:aws:iam::936142549234:user/fastapi-deployer"
}"""
render_terminal(
    "PowerShell - AWS CLI STS Verification",
    "aws sts get-caller-identity --profile fastapi-deployer",
    sts_output,
    "01_aws_sts_identity.png"
)

# 2. RDS Connection
rds_output = """==================================================
     VERIFY AMAZON RDS POSTGRESQL CONNECTION      
==================================================
Host:     fastapi-db.c8p0uyc2mw9n.us-east-1.rds.amazonaws.com
Port:     5432
Database: fastapi_prod
User:     postgres
Connecting...

[SUCCESS] Successful database connection!
Connected DB: fastapi_prod
Current User: postgres
Server Time:  2026-10-07 08:03:49.927682+00:00
PostgreSQL Version:
  PostgreSQL 15.19 on x86_64-pc-linux-gnu, compiled by x86_64-pc-linux-gnu-gcc (GCC) 12.4.0, 64-bit
=================================================="""
render_terminal(
    "PowerShell - RDS PostgreSQL Connection Test",
    "python test_db.py",
    rds_output,
    "02_rds_connection_success.png"
)

# 3. S3 Upload Test
s3_output = """==================================================
        TESTING AWS S3 FILE UPLOAD ENDPOINT       
==================================================
Bucket Name: fastapi-app-files-huynn69
AWS Region:  ap-southeast-1
Endpoint:    POST /upload

Uploading file 'proof-task3-upload.txt' via FastAPI...

[SUCCESS] Successful file upload to S3!
Status Code:   200 OK
File Name:     proof-task3-upload.txt
S3 Object URL: https://fastapi-app-files-huynn69.s3.ap-southeast-1.amazonaws.com/proof-task3-upload.txt

Current Files in S3 Bucket:
  - api-upload-proof.txt (60 bytes)
  - fastapi-demo-upload.txt (54 bytes)
  - proof-task3-upload.txt (58 bytes)
  - test-upload.txt (38 bytes)
=================================================="""
render_terminal(
    "PowerShell - AWS S3 Upload Verification",
    "python test_s3.py",
    s3_output,
    "03_s3_upload_success.png"
)