import telebot
from telebot import types
from user_register import user_register
from user_exists import user_exists
from question_register import question_register
from check_user_question_maker import user_check
import os
from dotenv import load_dotenv
from db_conection import cursor, conn
from AI_query import result
import datetime
from authentication import auth_user


token = os.getenv("TELE_BOT_KEY")
bot = telebot.TeleBot(token)


like = telebot.types.InlineKeyboardButton('می پسندم', callback_data='like')
dislike = telebot.types.InlineKeyboardButton('نمی پسندم', callback_data='dislike')
markup = telebot.types.InlineKeyboardMarkup()
markup.add(like, dislike)


# The following codes is callback section 
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data == 'like':
        like_sql = 'SELECT * FROM likes WHERE user_id=%s and question=%s'
        cursor.execute(like_sql, (user_id, msq))
        like_result = cursor.fetchone()
        if like_result is not None:
            bot.answer_callback_query(call.id, 'شما قبلا این سوال و پاسخ را پسندیده اید.\n از همراهی شما سپاسگذاریم', show_alert=True)
        elif like_result is None:
            bot.answer_callback_query(call.id, 'شما این سوال و پاسخ را پسندیدید.\n نظر شما ثبت شد', show_alert=True) 
            sql = 'SELECT * FROM question WHERE question=%s'
            cursor.execute(sql, (msq,))
            result = cursor.fetchone()
            if result is not None:
                result = result[5] 
                new_value = result + 1

                update_sql = 'UPDATE question SET likes=%s WHERE question=%s'
                cursor.execute(update_sql, (new_value, msq))
                conn.commit()
            
            like_sql_reg = 'INSERT INTO likes (user_id, created, question) VALUES (%s, %s, %s)'
            cursor.execute(like_sql_reg, (user_id, datetime.datetime.now(), msq))
            conn.commit()
        
    elif call.data == 'dislike':
        pass
# ---------> End callback section <---------

# The following section is for question maker
@bot.message_handler(commands=['QM'])
def questoin_maker(message):
    global user_id
    user_id = message.chat.id
    authenticate = auth_user(user_id)

    if authenticate==True:
        if user_check(user_id) == False:
            bot.send_message(message.chat.id, 'با عرض پوزش شما جزو طراحان سوال ما نیستید.')

        if user_check(user_id) == 'user no register':
            bot.send_message(message.chat.id, 'لطفا ابتدا ثبت نام کنید سپس اقدام به ثبت سوال کنید.')

        if user_check(user_id) == True:
            msg = bot.send_message(message.chat.id, 'مشکل یا تجربه خود را مطرح کنید.')
            bot.register_next_step_handler(msg, question)
    elif authenticate==False:
        bot.send_message(message.chat.id, 'حساب شما هنوز تایید اعتبار نشده است.')

def question(message):
    global qst
    qst = message.text
    msg = bot.send_message(message.chat.id, 'راه حل پیشنهادی برای تجربه شما چیست؟')
    bot.register_next_step_handler(msg, answer)

def answer(message):
    asw = message.text
    if question_register(qst, asw, user_id) == True:
        bot.send_message(message.chat.id, 'سوال|تجربه شما با موفقیت ثبت شد.')
    elif question_register(qst, asw, user_id) == False:
        bot.send_message(message.chat.id, 'خطایی در ثبت سوال رخ داده است.')

# ---------> End question maker section <---------


# The following section is the start and user registration section

@bot.message_handler(commands=['start'])
def register(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = types.KeyboardButton(text='ثبت نام در ربات', request_contact=True)
    markup.add(button)
    global user_id
    user_id = message.chat.id
    user = message.chat.id
    find_user = user_exists(user)

    if find_user == user:
        bot.send_message(message.chat.id, "\n سلام ، به ربات کمک یار کارمند بانک تجارت خوش آمدید."
                                        " قصد داریم با این ربات کمی از مشکلات کارمندان بکاهیم"
                                        " شما میتوانید مشکلات خود را بصورت سوال از ربات پرسیده  "
                                        "و در صورت وجود جواب در داده های ربات ،پاسخ نمایش داده میشود"
                                        "\n قبل از استفاده از ربات شما باید ثبت نام کنید و اطلاعات شما"
                                        "در پایگاه داده ی ما ثبت شود"
                                        "\n-/start شروع مسیر-شروع به کار ربات"
                                        "\n-/QM طراحی سوال"
                                        "\n-/help نکته های مفید کمکی",
                        reply_markup=markup)
    else:
        fu = find_user.strip()
        bot.send_message(message.chat.id, f"\n سلام {fu} عزیز ، به ربات کمک یار کارمند بانک تجارت خوش آمدید."
                                        " قصد داریم با این ربات کمی از مشکلات کارمندان بکاهیم"
                                        " شما میتوانید مشکلات خود را بصورت سوال از ربات پرسیده  "
                                        "و در صورت وجود جواب در داده های ربات ،پاسخ نمایش داده میشود"
                                        "\n در صورت عدم وجود جواب سوالی بصورت تصادفی نمایش داده میشود.\n"
                                        "\n-/start شروع مسیر-شروع به کار ربات"
                                        "\n-/QM طراحی سوال"
                                        "\n-/help نکته های مفید کمکی",
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

# ---------> End start and user registration section <---------
    

# The following section is help commands

@bot.message_handler(commands=['help', 'کمک'])
def register(message):
    bot.send_message(message.chat.id, '/start'
                     '\n/help'
                     '\n/QM -> question maker'
                     '\n/Contact'
                     '\nhello, hi, salam ...'
                     '\ntime, date, تاریخ',)

# ---------> End start and user registration section <---------


# The following section is where appropriate reactions are returned to user inputs

@bot.message_handler()
def hello_message(message):
    authenticate = auth_user(message.chat.id)

    if message.text in ['سلام', 'hi', 'hello', 'Hi', 'Hello', 'salam', 'چطوری']:
        bot.reply_to(message, "سلام به تو کارمند پرتلاش بانک تجارت")
    elif message.text in ['خسته', 'خسته شدم', 'خسته ام', 'خستگی', 'خسته نباشی', 'خسته ها',]:
        bot.reply_to(message, "واقعا خسته نباشی همکار عزیز، میدونم کارت سخت و طاقت فرساست ولی باید قوی باشی و به آینده روشن فکر کنی.")
    elif message.text in['date', 'time', 'تاریخ']:
        bot.reply_to(message, datetime.datetime.now())
    else:
        if authenticate==True:
            global user_id
            user_id = message.chat.id
            sql = 'SELECT * FROM question WHERE status=%s'
            cursor.execute(sql, (True,))

            results = cursor.fetchall()
            dataset = {}
            for data in results:
                dataset[data[1]] = f'{data[2]}\n \n \n تا الان {data[5]} کاربر این سوال و پاسخ را پسندیدند. '
            global msq
            msq, msa = result(message.text, dataset)
            bot.send_message(message.chat.id, f'سوالی که شما پرسیدید : {message.text} \n سوال مشابه در سرور : {msq} \n پاسخ : {msa}', reply_markup=markup)          
        elif authenticate==False:
            bot.send_message(message.chat.id, 'حساب شما هنوز تایید اعتبار نشده است.')

# ---------> End appropriate reactions section <---------


# The following section is for inline query settings

items = [
    {'id':'1', 
     'title':'Robot maker',
     'description':'I am Abbas Moradi, the creator of this robot. I hope that this robot will help you in solving work problems', 
     'message':'من عباس مرادی، هدف از نوشتن این ربات را بر پایه و اساس کمک به همکاران و دوستان خودم در استان قزوین قرار دادم و امیدوارم با این ربات بتوانم دین خودم را به دوستان و همکارانم، ادا کرده باشم.', 
     'thumbnail':'https://i.imgur.com/C9Zqgon.jpg'},
    {'id':'2', 
     'title':'بانک تجارت', 
     'description':'بانک تجارت، بانک فردا', 
     'message':'بانک تجارت، شرکت خدمات مالی و بانکداری ایرانی است. بانک تجارت بزرگ‌ترین بانک بورسی کشور، پس از انقلاب از ادغام چندین بانک تأسیس شد که قدیمی‌ترین آنها «بانک ایران و خاورمیانه» (پیشتر با نام بانک شاهنشاهی ایران) بود که از سال ۱۲۶۶ فعالیت داشت. طبق آمار سازمان مدیریت صنعتی کشور، هلدینگ بانک تجارت یکی از ۱۰۰شرکت برتر اقتصاد کشور شناخته شده‌است. اداره مرکزی بانک تجارت مستقر در برج تجارت شهر تهران می‌باشد. شعب، دفاتر و بانک‌های وابسته به بانک تجارت در خارج ازکشور درکشورهای فرانسه، جمهوری تاجیکستان، چین، انگلستان، امارات متحده عربی، آلمان و بلاروس درسطح بین‌المللی مشغول فعالیت می‌باشند. این بانک همچنین تنها بانکی است که هدف برنامه چهارم توسعه کشور در حمایت از بخش کشاورزی را محقق کرده‌است.بانک تجارت نخستین بانکی بود که از سیستم SGB استفاده نمود.', 
     'thumbnail':'https://i.imgur.com/sIXQJPT.png'},
    {'id':'3', 
     'title':'بهبود عملکرد', 
     'description':'در صورت تمایل به همکاری در بهبود عملکرد ربات با من در تماس باشید، 09362546408', 
     'message':'بنده برای بهبود عملکرد این ربات پذیرای پیشنهادات و نظرات شما عزیزان هستم.', 
     'thumbnail':'https://i.imgur.com/oHyfoFt.jpg'}
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
# ---------> End inline query section <---------


bot.infinity_polling(none_stop=True)