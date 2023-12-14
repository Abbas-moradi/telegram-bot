import psycopg2
import os
from dotenv import load_dotenv


dotenv_path = ".env"
load_dotenv(dotenv_path)



db_config = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()