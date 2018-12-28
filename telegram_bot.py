import os
import subprocess
from telebot import TeleBot
from threading import Event
from config import config
from image_capture import ImageCapture
from motion_monitor import MotionMonitor


root = os.path.dirname(os.path.abspath(__file__))
bot_conf = config(os.path.join(root, 'config.json')).get_config()
telebot = TeleBot(token=bot_conf['TELEGRAM'].get("BOT_API_TOKEN", ""), threaded=False)
messages = bot_conf['TELEGRAM_MESSAGES']
image_capture = ImageCapture()


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

@telebot.message_handler(commands=['capture'])
def capture(message):
    telebot.send_photo(bot_conf['TELEGRAM'].get("BOT_ID", ""),
                       image_capture.capture())

@telebot.message_handler(commands=['capture_sample'])
def capture_sample(message):
    s = image_capture.capture_video(10)
    destiny_path = os.path.join(root, "tmp.h264")
    mp4_destiny_path = destiny_path[:destiny_path.rfind('.')] + 'mp4'
    image_capture.write_stream(s, destiny_path)
    command = [
        'MP4Box',
        '-add',
        destiny_path,
        mp4_destiny_path
    ]
    if subprocess.call(command) == 0:
        telebot.send_video(bot_conf['TELEGRAM'].get("BOT_ID", ""),
                           open(mp4_destiny_path, 'rb').read())
        if os.path.exists(mp4_destiny_path):
            os.remove(mp4_destiny_path)
        if os.path.exists(destiny_path):
            os.remove(destiny_path)

@telebot.message_handler(commands=['is_alive'])
def is_alive(message):
    telebot.reply_to(message, messages.get("IS_ALIVE", ""))

stopper = Event()
motion_monitor = MotionMonitor(stopper, capture)
motion_monitor.start()

telebot.polling(interval=0.1)
stopper.set()