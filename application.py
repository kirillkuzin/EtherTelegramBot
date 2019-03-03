import telebot
import os
from settings import *
from flask import Flask, request

bot = telebot.TeleBot(BOT_TOKEN)
application = Flask(__name__)

chatIds = {}

@bot.message_handler(commands = ['start'])
def startMessage(message):
    bot.send_message(message.chat.id, 'Start')

@bot.message_handler(func=lambda message: True)
def textMessage(message):
    chatIds.update({message.text: message.chat.id})
    bot.send_message(message.chat.id, 'Key updated')

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
    addressFrom = request.form.get('from')
    addressTo = request.form.get('to')
    value = request.form.get('value')
    bot.send_message(chatIds.get(addressFrom), addressFrom + ' ' + addressTo + ' ' + value)

if __name__ == '__main__':
    if DEBUG_MODE:
        bot.polling()
    else:
        application.run(
            host = '0.0.0.0',
            port = int(os.environ.get('PORT', 5000))
        )
