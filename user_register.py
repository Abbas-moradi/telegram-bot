import psycopg2
import os


db_config = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT', '5432'),
}

# conn = psycopg2.connect(**db_config)
# cursor = conn.cursor()


def user_register(user_info, *args, **kwargs):
    sql = "INSERT INTO users (user_id, first_name, last_name, phone, vcard, questoin_maker) VALUES (%s, %s, %s, %s, %s)"
    values = (user_info['user_id'], user_info['first_name'], 
              user_info['last_name'], user_info['phone_number'],
              user_info['vcard'], 'False')

    try:
        cursor.execute(sql, values)
        conn.commit()
        bot.send_message(message.chat.id, "اطلاعات شما با موفقیت ذخیره شد.")
    except Exception as e:
        conn.rollback()
        bot.send_message(message.chat.id, "خطا در ذخیره اطلاعات در دیتابیس.")