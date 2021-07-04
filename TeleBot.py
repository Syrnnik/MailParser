import telebot
from telebot import *
from configparser import ConfigParser
from MailParser import *

proc = False

config = ConfigParser()
config.read("./botConf.ini")

eml = MailParser()
sleep_time = int(config['TeleBot']['sleepTime'])

token = config['TeleBot']['token']
bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def update_mail(msg):
    chat_id = msg.chat.id
    # print(chat_id)

    bot.send_message(chat_id, "Session is started. Send `/end` to finish session.", parse_mode="Markdown")

    global proc
    proc = True
    eml.login()

    while proc:
        photos, videos, music, docs = eml.get_mail_attaches()

        for photo in photos:
            bot.send_photo(chat_id, photo, timeout=10000)

        for video in videos:
            bot.send_video(chat_id, video, timeout=50000)

        for mus in music:
            bot.send_audio(chat_id, mus, timeout=10000)

        for doc in docs:
            bot.send_document(chat_id, doc, timeout=50000)

        time.sleep(sleep_time)


@bot.message_handler(commands=['end'])
def end_update(msg):
    chat_id = msg.chat.id

    global proc
    proc = False

    bot.send_message(chat_id, "Session is ended. Send `/start` to start session.", parse_mode="Markdown")


bot.polling()
eml.logout()

# https://www.t.me/Syrn_Bot