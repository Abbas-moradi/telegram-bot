import psycopg2
import os


db_config = {
    'dbname': "tejarat_bot",
    'user': "postgres",
    'password': "@bb@s1366",
    'host': "localhost",
    'port': '5432',
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()