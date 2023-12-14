import telebot
from telebot import types
from user_register import user_register
from user_exists import user_exists
from question_register import question_register
from check_user_question_maker import user_check
import os


# bot = telebot.TeleBot(os.environ.get('TELE_BOT_KEY')) 
bot = telebot.TeleBot(token='6547851672:AAEJP4ES9iZgIcJcfYj8PiIhopwTpj0UM5I')


# The following section is for question maker

@bot.message_handler(commands=['QM'])
def questoin_maker(message):
    global user
    user = message.chat.id

    if user_check(user) == False:
        bot.send_message(message.chat.id, 'با عرض پوزش شما جزو طراحان سوال ما نیستید.')

    if user_check(user) == 'user no register':
        bot.send_message(message.chat.id, 'لطفا ابتدا ثبت نام کنید سپس اقدام به ثبت سوال کنید.')

    if user_check(user) == True:
        msg = bot.send_message(message.chat.id, 'مشکل یا تجربه خود را مطرح کنید.')
        bot.register_next_step_handler(msg, question)

def question(message):
    global qst
    qst = message.text
    msg = bot.send_message(message.chat.id, 'راه حل پیشنهادی برای تجربه شما چیست؟')
    bot.register_next_step_handler(msg, answer)

def answer(message):
    asw = message.text
    if question_register(qst, asw, user) == True:
        bot.send_message(message.chat.id, 'سوال شما با موفقیت ثبت شد.')
    elif question_register(qst, asw, user) == False:
        bot.send_message(message.chat.id, 'خطایی در ثبت سوال رخ داده است.')


@bot.message_handler(commands=['start'])
def register(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = types.KeyboardButton(text='ثبت نام در ربات', request_contact=True)
    markup.add(button)
    user = message.chat.id
    find_user = user_exists(user)

    if find_user == user:
        bot.send_message(message.chat.id, "\n سلام ، به ربات کمک یار کارمند بانک تجارت خوش آمدید."
                                        " قصد داریم با این ربات کمی از مشکلات کارمندان بکاهیم"
                                        " شما میتوانید مشکلات خود را بصورت سوال از ربات پرسیده  "
                                        "و در صورت وجود جواب در داده های ربات ،پاسخ نمایش داده میشود"
                                        "\n قبل از استفاده از ربات شما باید ثبت نام کنید و اطلاعات شما"
                                        "در پایگاه داده ی ما ثبت شود",
                        reply_markup=markup)
    else:
        fu = find_user.strip()
        bot.send_message(message.chat.id, f"\n سلام {fu} عزیز ، به ربات کمک یار کارمند بانک تجارت خوش آمدید."
                                        " قصد داریم با این ربات کمی از مشکلات کارمندان بکاهیم"
                                        " شما میتوانید مشکلات خود را بصورت سوال از ربات پرسیده  "
                                        "و در صورت وجود جواب در داده های ربات ،پاسخ نمایش داده میشود",
                        )
    

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


# The following section is for inline query settings

items = [
    {'id':'1', 'title':'Robot maker', 'description':'I am Abbas Moradi, the creator of this robot \nI hope that this robot will help you in solving work problems', 'message':'', 'thumbnail':'https:\\i.imgur.com\C9Zqgon.jpg'},
    {'id':'2', 'title':'بانک تجارت', 'description':'بانک تجارت، بانک فردا', 'message':'', 'thumbnail':'https:\\i.imgur.com\sIXQJPT.png'},
    {'id':'3', 'title':'بهبود عملکرد', 'description':'در صورت تمایل به همکاری در بهبود عملکرد ربات با من در تماس باشید، 09362546408', 'message':'', 'thumbnail':'https:\\i.imgur.com\oHyfoFt.jpg'}
    ]

@bot.inline_handler(lambda query: len(query.query)==0)
def handle_inline_query(query):
    results = []

    for item in items:
        result = types.InlineQueryResultArticle(
            id=item['id'],
            title=item['title'],
            description=item['description'],
            input_message_content=types.InputTextMessageContent(
                message_text=item['message']
            ),
            thumbnail_url=item['thumbnail']
        )
        results.append(result)
    
    bot.answer_inline_query(query.id, results)



bot.infinity_polling(none_stop=True)