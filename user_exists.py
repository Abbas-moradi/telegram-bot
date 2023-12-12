from user_register import conn, cursor


def user_exists(id):
    check_query = "SELECT * FROM user_info WHERE user_id = %s"
    cursor.execute(check_query, (id,))

    result = cursor.fetchone()

    if result:
        return result[1]
    else:
        return id

    