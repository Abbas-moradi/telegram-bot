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


def question_register(*args, **kwargs):
    question , answer = args[0], args[1]
    print(f'Questio: {question} \nAnswer: {answer}')