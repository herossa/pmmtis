import os
from telebot import TeleBot
from config import config

root = os.path.dirname(os.path.abspath(__file__))
bot_conf = config(os.path.join(root, 'config.json')).get_config()
telebot = TeleBot(token=bot_conf['TELEGRAM'].get("BOT_API_TOKEN", ""))
messages = bot_conf['TELEGRAM_MESSAGES']

@telebot.message_handler(commands=['start'])
def start(message):
    telebot.reply_to(message, messages.get("START", ""))

@telebot.message_handler(commands=['help'])
def help(message):
    help = messages.get("HELP", "")
    for h in messages.get("HELP_COMMANDS", []):
        help += "\n    "
        help += h
    telebot.reply_to(message, help)

@telebot.message_handler(commands=['capture']):
def capture(message):
    #captura uma imagem e envia 
    pass

telebot.polling()