import telebot
import os
from settings import *
from flask import Flask, request

bot = telebot.TeleBot(BOT_TOKEN)
application = Flask(__name__)

@bot.message_handler(commands = ['start'])
def startMessage(message):
    bot.send_message(message.chat.id, 'Start')

@application.route('/' + BOT_TOKEN, methods = ['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '!', 200

@application.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url = WEBHOOK_LINK + BOT_TOKEN)
    return '!', 200

@application.route('/tx')
def tx():
    pass

if __name__ == '__main__':
    if DEBUG_MODE:
        bot.polling()
    else:
        application.run(
            host = '0.0.0.0',
            port = int(os.environ.get('PORT', 5000))
        )
