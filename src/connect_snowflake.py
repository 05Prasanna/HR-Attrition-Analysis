import os
from pathlib import Path
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd

# Explicit .env path
ENV_PATH = Path("/Users/prasanna/Desktop/hr_attrition/.env")

load_dotenv(dotenv_path=ENV_PATH, override=True)

# Read credentials
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")

# Check credentials
print("Checking Snowflake credentials...")

for name, value in {
    "USER": user,
    "PASSWORD": password,
    "ACCOUNT": account,
    "WAREHOUSE": warehouse,
    "DATABASE": database,
    "SCHEMA": schema
}.items():
    print(f"{name}: {'LOADED' if value else 'MISSING'}")

if not all([user, password, account, warehouse, database, schema]):
    raise ValueError("Missing Snowflake environment variables.")

# Connect
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema,
    enable_server_session_keep_alive_auto_detection=True
)

print("Snowflake connected successfully!")

query = "SELECT * FROM hr_attrition_final"

df = pd.read_sql(query, conn)

print("Dataset Shape:", df.shape)
print(df.head())

conn.close()