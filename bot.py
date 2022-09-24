from email import message
import logging
from urllib import request
from random import randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
logging.basicConfig(filename="bot.log", level=logging.INFO)

# PROXY = {'proxy_url': settings.PROXY_URL,
#     'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print("Вызван /start")
    # print(update) 
    update.message.reply_text("Привет")

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def play_random_numbers(user_number):
    bot_number = randint(user_number - 100, user_number + 100)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, вы выиграли"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, ничья"  
    else:
        message = f"Ваше число {user_number}, моё {bot_number}, вы проиграли"
    return message

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)

def main():
    mybot = Updater(settings.API_KEY, use_context=True)  
    # request_kwargs=PROXY
    
    md = mybot.dispatcher
    md.add_handler(CommandHandler('start', greet_user))
    md.add_handler(CommandHandler('guess', guess_number))
    md.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot starting")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()