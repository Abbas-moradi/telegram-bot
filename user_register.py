from db_conection import cursor, conn


def user_register(user_info, *args, **kwargs):
    check_query = "SELECT EXISTS (SELECT 1 FROM user_info WHERE user_id = %s)"
    check_values = (user_info['user_id'],)

    cursor.execute(check_query, check_values)
    record_exists = cursor.fetchone()[0]

    if record_exists:
        return 'exists'
    
    sql = "INSERT INTO user_info (user_id, first_name, last_name, phone_number, vcard, questoin_maker) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (
        user_info['user_id'], 
        user_info['first_name'], 
        user_info['last_name'], 
        user_info['phone_number'],
        user_info['vcard'], 
        'False'
        )
    
    try:
        cursor.execute(sql, values)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
        