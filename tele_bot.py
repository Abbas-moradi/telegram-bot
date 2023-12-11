import telebot
from telebot import types
from user_register import user_register
import os


bot = telebot.TeleBot(os.environ.get('TELE_BOT_KEY'))


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
    contact_info = {}
   
    contact_info['user_id']= message.contact.user_id
    contact_info['first_name']= message.contact.first_name
    contact_info['last_name']= message.contact.last_name
    contact_info['phone_number']= message.contact.phone_number
    contact_info['vcard']= message.contact.vcard
    
    if user_register(contact_info)==True:
        bot.send_message(message.chat.id, "اطلاعات شما با موفقیت ذخیره شد.")
    elif user_register(contact_info)=='exists':
        bot.send_message(message.chat.id, "شما قبلا ثبت نام کرده اید.")
    else:
        bot.send_message(message.chat.id, "خطا در ذخیره اطلاعات در دیتابیس.") 
    

@bot.message_handler()
def hello_message(message):
    if message.text in ['سلام', 'hi', 'hello', 'Hi', 'Hello', 'salam', 'چطوری']:
        bot.reply_to(message, "سلام به تو کارمند پرتلاش بانک تجارت")

bot.infinity_polling(none_stop=True)
