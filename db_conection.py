import psycopg2
import os




db_config = {
    'dbname': os.environ.get("DB_NAME"),
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASSWORD"),
    'host': os.environ.get("DB_HOST"),
    'port': os.environ.get("DB_PORT"),
}

# db_config = {
#     'dbname': "tejarat_bot",
#     'user': "postgres",
#     'password': "@bb@s1366",
#     'host': "localhost",
#     'port': '5432',
# }
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()