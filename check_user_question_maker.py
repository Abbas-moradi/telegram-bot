from user_register import conn, cursor


def user_check(id):
    check_query = "SELECT * FROM user_info WHERE user_id = %s"
    cursor.execute(check_query, (id,))

    result = cursor.fetchone()

    if not result:
        return 'user no register'
    elif result[-1]==False:
        return False
    elif result[-1]==True:
        return True

    