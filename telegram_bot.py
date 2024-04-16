import os
import telebot
from EmployerGPT import EmployerGPT
from dotenv import load_dotenv
load_dotenv()


class Tele:
    API_TOKEN = os.getenv("TG_BOT_TOKEN")
    bot = telebot.TeleBot(API_TOKEN)
    participants = set()

    @staticmethod
    @bot.message_handler(commands=['start'])
    def _start(message):
        Tele.bot.reply_to(message, "Привет! Для начала общения введите /join чтобы присоединиться к беседе.")

    @staticmethod
    @bot.message_handler(commands=['join'])
    def _join_chat(message):
        if message.chat.id in Tele.participants:
            return
        Tele.bot.send_message(message.chat.id, "В этом чате присутствуют:")
        for participant in Tele.participants:
            Tele.bot.send_message(participant, f"{message.chat.id} присоединился")
            Tele.bot.send_message(message.chat.id, f"{participant}")
        Tele.participants.add(message.chat.id)
        Tele.bot.reply_to(message, "Вы присоединились к беседе.")

    @staticmethod
    @bot.message_handler(commands=['leave'])
    def _leave_chat(message):
        if message.chat.id not in Tele.participants:
            return
        Tele.participants.remove(message.chat.id)
        for participant in Tele.participants:
            Tele.bot.send_message(participant, f"{message.chat.id} покинул беседу")
        Tele.bot.reply_to(message, "Вы покинули беседу.")

    @staticmethod
    @bot.message_handler(func=lambda message: True)
    def _echo_all(message):
        if message.from_user.is_bot:
            return

        for participant in Tele.participants:
            if participant != message.chat.id:
                Tele.bot.send_message(participant, message.text)

    @staticmethod
    def start_polling():
        Tele.bot.polling()
