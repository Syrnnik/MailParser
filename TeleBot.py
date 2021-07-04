import telebot
from telebot import *
from configparser import ConfigParser
from MailParser import *
import time

proc = False
host = ''
username = ''
password = ''

mailConf = ConfigParser()
mailConf.read("./mailConf.ini")

config = ConfigParser()
config.read("./botConf.ini")

eml = MailParser()

bot = TeleBot(config.get('TeleBot', 'token'))


def save_mailConf():
    with open("./mailConf.ini", 'w') as mailConf_file: mailConf.write(mailConf_file)


def add_user(id, host, username, password):
    mailConf.add_section(id)
    mailConf.set(id, 'host', host)
    mailConf.set(id, 'username', username)
    mailConf.set(id, 'password', password)
    save_mailConf()


def checkMail(chat_id):
    if str(chat_id) in mailConf: return True
    return False


@bot.message_handler(commands=['start'])
def start(msg):
    chat_id = msg.chat.id

    info_msg = """*Commands:*
/start - see this message.
/register - register your email.
/profile - see your email information.
/changeemail - change profile email.
/changepass - change profile password.
/runsession - start checking email for new messages.
/stopsession - stop checking email.
"""

    return bot.send_message(chat_id, info_msg, parse_mode="Markdown")


@bot.message_handler(commands=['register'])
def register(msg):
    chat_id = msg.chat.id

    if checkMail(chat_id):
        return bot.send_message(chat_id, "You already registered. Send /profile to see information.", parse_mode="Markdown")
    
    reply_msg = bot.send_message(chat_id, "Let's register!\nEnter your email address", parse_mode="Markdown")
    bot.register_next_step_handler(reply_msg, enter_email)

def enter_email(msg):
    chat_id = msg.chat.id

    global username
    username = msg.text

    reply_msg = bot.send_message(chat_id, "Okey, now enter your IMAP password", parse_mode="Markdown")
    bot.register_next_step_handler(reply_msg, enter_password)

def enter_password(msg):
    chat_id = msg.chat.id

    global password
    password = msg.text

    global host
    global username
    host = 'imap.' + username.split('@')[1]

    add_user(str(chat_id), host, username, password)

    email_info = f"""*Your email profile:*
username - `{username}`
password - `{password}`
"""

    return bot.send_message(chat_id, f"Good. Your address successfully created.\n{email_info}", parse_mode="Markdown")


@bot.message_handler(commands=['changeemail'])
def changeemail(msg):
    chat_id = msg.chat.id

    if not checkMail(chat_id):
        return bot.send_message(chat_id, "You're not registered. Send /register to to create profile.", parse_mode="Markdown")

    reply_msg = bot.send_message(chat_id, "Enter new email address", parse_mode="Markdown")
    bot.register_next_step_handler(reply_msg, new_email)

def new_email(msg):
    chat_id = msg.chat.id

    host = 'imap.' + msg.text.split('@')[1]

    new_email = msg.text
    mailConf.set(str(chat_id), 'host', host)
    user_name = mailConf.set(str(chat_id), 'username', new_email)
    user_pass = mailConf.get(str(chat_id), 'password')
    save_mailConf()

    email_info = f"""*Your email profile:*
username - `{new_email}`
password - `{user_pass}`
"""

    return bot.send_message(chat_id, f"Your email successfully changed.\n{email_info}", parse_mode="Markdown")


@bot.message_handler(commands=['changepass'])
def changepass(msg):
    chat_id = msg.chat.id

    if not checkMail(chat_id):
        return bot.send_message(chat_id, "You're not registered. Send /register to to create profile.", parse_mode="Markdown")

    reply_msg = bot.send_message(chat_id, "Enter new password address", parse_mode="Markdown")
    bot.register_next_step_handler(reply_msg, new_pass)

def new_pass(msg):
    chat_id = msg.chat.id

    new_pass = msg.text
    user_name = mailConf.get(str(chat_id), 'username')
    user_pass = mailConf.set(str(chat_id), 'password', new_pass)

    email_info = f"""*Your email profile:*
username - `{user_name}`
password - `{new_pass}`
"""

    return bot.send_message(chat_id, f"Your password successfully changed.\n{email_info}", parse_mode="Markdown")


@bot.message_handler(commands=['profile'])
def profile(msg):
    chat_id = msg.chat.id

    if not checkMail(chat_id):
        return bot.send_message(chat_id, "You're not registered. Send /register to to create profile.", parse_mode="Markdown")

    user_name = mailConf.get(str(chat_id), 'username')
    user_pass = mailConf.get(str(chat_id), 'password')

    email_info = f"""*Your email profile:*
username - `{user_name}`
password - `{user_pass}`
"""

    return bot.send_message(chat_id, email_info, parse_mode="Markdown")


@bot.message_handler(commands=['runsession'])
def update_mail(msg):
    chat_id = msg.chat.id

    if not checkMail(chat_id):
        return bot.send_message(chat_id, "You're not registered. Send /register to to create profile.", parse_mode="Markdown")

    user_host = mailConf.get(str(chat_id), 'host')
    user_name = mailConf.get(str(chat_id), 'username')
    user_pass = mailConf.get(str(chat_id), 'password')

    email_info = f"""*Email info:*
username - `{user_name}`
password - `{user_pass}`
"""

    bot.send_message(chat_id, f"Session is started.\n\n{email_info}\nSend /stopsession to finish session.", parse_mode="Markdown")

    global proc
    proc = True
    eml.login(user_host, user_name, user_pass)

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

        time.sleep(30)
    
    return eml.logout()


@bot.message_handler(commands=['stopsession'])
def end_update(msg):
    chat_id = msg.chat.id

    if not checkMail(chat_id):
        return bot.send_message(chat_id, "You're not registered. Send /register to to create profile.", parse_mode="Markdown")

    global proc
    proc = False

    return bot.send_message(chat_id, "Session is ended. Send /startsession to start session.", parse_mode="Markdown")


bot.polling()