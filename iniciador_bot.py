import telebot
from mysql.config import TG_TOKEN


def create_bot_instance():
    try:
        bot = telebot.TeleBot(TG_TOKEN)
        print('Bot is running...')
        return bot 

    except Exception as e:
        print("Error initializing bot:", e)
        exit(1)

bot = create_bot_instance()
