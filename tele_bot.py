import telebot

bot = telebot.TeleBot('6547851672:AAF46rU-DYL6obqQJtB60ZS2EqbFxzUG-HM')

Introducing = telebot.types.InlineKeyboardButton("سازنده ربات", url="https://github.com/Abbas-moradi")
tejarat = telebot.types.InlineKeyboardButton("بانک تجارت", url="https://tejaratbank.ir")
markup = telebot.types.InlineKeyboardMarkup()
markup.add(Introducing, tejarat)


@bot.message_handler(commands=['start'])
def get_number(message):
    bot.send_message(message.chat.id, " سلام ، به ربات کمک یار کارمند بانک تجارت خوش آمدید."
                                    " قصد داریم با این ربات کمی از مشکلات کارمندان بکاهیم"
                                    " شما میتوانید مشکلات خود را بصورت سوال از ربات پرسیده  "
                                    "و در صورت وجود جواب در داده های ربات ،پاسخ نمایش داده میشود", 
                     reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, "چجوری میتونم کمکت کنم؟؟؟")

@bot.message_handler()
def help_message(message):
    if message.text in ['سلام', 'hi', 'hello', 'Hi', 'Hello', 'salam', 'چطوری']:
        bot.reply_to(message, "سلام به تو کارمند پرتلاش بانک تجارت")

bot.infinity_polling()