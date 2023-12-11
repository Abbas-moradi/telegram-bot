import telebot

bot = telebot.TeleBot('6547851672:AAF46rU-DYL6obqQJtB60ZS2EqbFxzUG-HM')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, "چجوری میتونم کمکت کنم؟؟؟")

@bot.message_handler()
def help_message(message):
    if message.text in ['سلام', 'hi', 'hello', 'Hi', 'Hello', 'salam', 'چطوری']:
        bot.reply_to(message, "سلام به تو کارمند پرتلاش بانک تجارت")

bot.infinity_polling()