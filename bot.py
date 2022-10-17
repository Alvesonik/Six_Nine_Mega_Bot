from email import message
import logging
from urllib import request
from emoji import emojize
from glob import glob
from random import randint, choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
logging.basicConfig(filename="bot.log", level=logging.INFO)

# PROXY = {'proxy_url': settings.PROXY_URL,
#     'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print("Вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Привет пользователь {context.user_data['emoji']}")

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {context.user_data['emoji']}")

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji'] 

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

def send_mem(update, context):
    mem_photo_list = glob("images/mem*.jp*g")
    mem_photo_filename = choice(mem_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(mem_photo_filename, 'rb'))

def main():
    mybot = Updater(settings.API_KEY, use_context=True)  
    # , request_kwargs=PROXY
    
    md = mybot.dispatcher
    md.add_handler(CommandHandler("start", greet_user))
    md.add_handler(CommandHandler("play", play_random_numbers))         
    md.add_handler(CommandHandler("guess", guess_number))
    md.add_handler(CommandHandler("photo", send_mem))
    md.add_handler(CommandHandler("emoji", get_smile))       
    md.add_handler(MessageHandler(Filters.text, talk_to_me))    

    logging.info("Bot starting")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()