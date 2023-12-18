from db_conection import conn, cursor


def auth_user(id):
    sql = 'SELECT * FROM user_info WHERE user_id=%s'
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    if result[7]==True:
        return True
    elif result[7]==False:
        return False