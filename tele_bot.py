import telebot
from telebot import types
import psycopg2


bot = telebot.TeleBot('6547851672:AAF46rU-DYL6obqQJtB60ZS2EqbFxzUG-HM')

db_config = {
    'dbname': 'database_name',
    'user': 'database_user',
    'password': 'database_password',
    'host': 'localhost',
    'port': '5432',
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def register(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = types.KeyboardButton(text='ثبت نام در ربات', request_contact=True)
    markup.add(button)

    bot.send_message(message.chat.id, "\n سلام ، به ربات کمک یار کارمند بانک تجارت خوش آمدید."
                                    " قصد داریم با این ربات کمی از مشکلات کارمندان بکاهیم"
                                    " شما میتوانید مشکلات خود را بصورت سوال از ربات پرسیده  "
                                    "و در صورت وجود جواب در داده های ربات ،پاسخ نمایش داده میشود"
                                    "\n قبل از استفاده از ربات شما باید ثبت نام کنید و اطلاعات شما"
                                    "در پایگاه داده ی ما ثبت شود",
                     reply_markup=markup)
    

@bot.message_handler(content_types=['contact'])
def contact_register(message):
    print(message.contact)
    sql = "INSERT INTO users (user_id, first_name, last_name, phone, vcard, questoin_maker) VALUES (%s, %s, %s, %s, %s)"
    values = (message.contact['user_id'], message.contact['first_name'], 
              message.contact['last_name'], message.contact['phone_number'],
              message.contact['vcard'], 'False')

    try:
        cursor.execute(sql, values)
        conn.commit()
        bot.send_message(message.chat.id, "اطلاعات شما با موفقیت ذخیره شد.")
    except Exception as e:
        conn.rollback()
        bot.send_message(message.chat.id, "خطا در ذخیره اطلاعات در دیتابیس.")

@bot.message_handler()
def hello_message(message):
    if message.text in ['سلام', 'hi', 'hello', 'Hi', 'Hello', 'salam', 'چطوری']:
        bot.reply_to(message, "سلام به تو کارمند پرتلاش بانک تجارت")

bot.infinity_polling(none_stop=True)