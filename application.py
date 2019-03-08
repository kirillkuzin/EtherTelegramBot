import telebot
import os
from settings import BOT_TOKEN, WEBHOOK_LINK, DEBUG_MODE
from flask import Flask, request
from ethereum_core import Ethereum
from redis_core import Redis

bot = telebot.TeleBot(BOT_TOKEN)
application = Flask(__name__)
ethereum = Ethereum()
redis = Redis()

chatIds = {}

@bot.message_handler(commands = ['start'])
def startMessage(message):
    bot.send_message(message.chat.id, 'Start')

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    parsedData = call.data.split(' ')
    status = parsedData[0]
    txId = int(parsedData[1])
    if status == 'confirmed':
        tx = redis.getTx(txId)

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

@application.route('/tx', methods = ['POST'])
def tx():
    fromAddress = str(request.form.get('from'))
    toAddress = str(request.form.get('to'))
    value = int(request.form.get('value'))
    data = str(request.form.get('data'))
    tx = ethereum.buildTransaction(fromAddress, toAddress, value)
    txId = redis.addNewTx(tx)
    bot.send_message(0, 'New tx:', reply_markup = acceptTxMarkup(txId))
    return '', 200

if __name__ == '__main__':
    if DEBUG_MODE:
        bot.remove_webhook()
        bot.polling()
    else:
        application.run(
            host = '0.0.0.0',
            port = int(os.environ.get('PORT', 5000))
        )
