import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "fastapi-db.c8p0uyc2mw9n.us-east-1.rds.amazonaws.com")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fastapi_prod")

print("==================================================")
print("     VERIFY AMAZON RDS POSTGRESQL CONNECTION      ")
print("==================================================")
print(f"Host:     {DB_HOST}")
print(f"Port:     {DB_PORT}")
print(f"Database: {DB_NAME}")
print(f"User:     {DB_USER}")
print("Connecting...")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();")).scalar()
        db_now = connection.execute(text("SELECT current_database(), current_user, now();")).fetchone()
        print("\n[SUCCESS] Successful database connection!")
        print(f"Connected DB: {db_now[0]}")
        print(f"Current User: {db_now[1]}")
        print(f"Server Time:  {db_now[2]}")
        print(f"PostgreSQL Version:\n  {result}")
        print("==================================================")
except Exception as e:
    print(f"\n[FAILED] Connection error: {e}")
    sys.exit(1)