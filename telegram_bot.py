import os
import telebot
from EmployerGPT import EmployerGPT
from dotenv import load_dotenv
load_dotenv()


class Tele:
    API_TOKEN = os.getenv("TG_BOT_TOKEN")
    bot = telebot.TeleBot(API_TOKEN)
    participants = []
    n = 2
    employer = EmployerGPT(["Здравствуйте"] * n, 'logs.txt')

    @staticmethod
    @bot.message_handler(commands=['start'])
    def _start(message):
        Tele.bot.reply_to(message, "Привет! Для начала общения введите /join чтобы присоединиться к беседе.")

    @staticmethod
    @bot.message_handler(commands=['join'])
    def _join_chat(message):
        if message.chat.id in Tele.participants or len(Tele.participants) >= Tele.n:
            return
        Tele.bot.send_message(message.chat.id, "В этом чате присутствуют:")
        for participant in Tele.participants:
            Tele.bot.send_message(participant, f"{message.chat.id} присоединился")
            Tele.bot.send_message(message.chat.id, f"{participant}")
        Tele.bot.reply_to(message, f"Вы присоединились к беседе под номером {len(Tele.participants)}")
        Tele.participants.append(message.chat.id)
        if len(Tele.participants) >= Tele.n:
            who, reply = Tele.employer.say_first_sentence()
            for participant_num in range(len(Tele.participants)):
                Tele.bot.send_message(Tele.participants[participant_num], text=f"Сообщение для {who}: {reply}")

    @staticmethod
    @bot.message_handler(commands=['leave'])
    def _leave_chat(message):
        if message.chat.id not in Tele.participants:
            return
        Tele.participants.remove(message.chat.id)
        for participant in Tele.participants:
            Tele.bot.send_message(participant, f"{message.chat.id} покинул беседу")
        Tele.bot.reply_to(message, "Вы покинули беседу.")
        Tele.employer.delete_person(Tele.participants.index(message.chat.id))

    @staticmethod
    @bot.message_handler(func=lambda message: True)
    def _echo_all(message):
        if message.from_user.is_bot:
            return

        person_number = Tele.participants.index(message.chat.id)
        who, reply = Tele.employer.answer_on_message(person_number, message.text)
        for participant_num in range(len(Tele.participants)):
            participant = Tele.participants[participant_num]
            if participant != message.chat.id:
                Tele.bot.send_message(participant, f"{person_number}: {message.text}")
            Tele.bot.send_message(Tele.participants[participant_num], text=f"Сообщение для {who}: {reply}")

    @staticmethod
    def start_polling():
        Tele.bot.polling()
