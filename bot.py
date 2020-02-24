import telebot

bot = telebot.TeleBot('1092070603:AAFfQNIq8vkm6DkGgj2oOU5OgsDnPLzBonE')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

bot.polling()
