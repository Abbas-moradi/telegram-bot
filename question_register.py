from db_conection import cursor, conn
from datetime import datetime


def question_register(*args, **kwargs):
    question , answer, id = args[0], args[1], args[2]
    date_now = datetime.now()
    print(f'Questio: {question} \nAnswer: {answer}')
    sql = "INSERT INTO question (question, answer, created, user_id_creator) VALUES (%s, %s, %s, %s)"
    values = (
        question,
        answer,
        date_now,
        id
        )
    
    try:
        cursor.execute(sql, values)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False