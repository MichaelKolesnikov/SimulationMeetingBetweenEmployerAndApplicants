import os
import telebot
from EmployerGPT import EmployerGPT
from dotenv import load_dotenv
load_dotenv()


class Participant:
    def __init__(self, name: str, identifier: int):
        self.name = name
        self.identifier = identifier


class Tele:
    API_TOKEN = os.getenv("TG_BOT_TOKEN")
    bot = telebot.TeleBot(API_TOKEN)
    participants: list[Participant] = []
    n = 2
    employer: EmployerGPT = EmployerGPT([f"Name_{i}" for i in range(n)], ["Здравствуйте"] * n, 'logs.txt')

    @staticmethod
    @bot.message_handler(commands=['start'])
    def _start(message):
        Tele.bot.reply_to(message, "Привет! Для начала общения введите /join чтобы присоединиться к беседе.")

    @staticmethod
    @bot.message_handler(commands=['join'])
    def _join_chat(message):
        if len(Tele.participants) >= Tele.n or any(list(map(lambda x: x.identifier == message.chat.id, Tele.participants))):
            return
        current_number = len(Tele.participants)
        Tele.bot.send_message(message.chat.id, f"В этом чате присутствуют: {list(map(lambda x: x.name, Tele.participants))}")
        for participant in Tele.participants:
            Tele.bot.send_message(participant.identifier, f"{current_number} присоединился")
        Tele.bot.reply_to(message, f"Вы присоединились к беседе под номером {current_number}")
        Tele.participants.append(Participant(f"Name_{current_number}", message.chat.id))
        if len(Tele.participants) >= Tele.n:
            who, reply = Tele.employer.say_first_sentence()
            for participant_num in range(len(Tele.participants)):
                Tele.bot.send_message(Tele.participants[participant_num].identifier, text=f"Сообщение для {who}: {reply}")

    @staticmethod
    @bot.message_handler(commands=['leave'])
    def _leave_chat(message):
        index = 0
        while index < len(Tele.participants) and Tele.participants[index].identifier != message.chat.id:
            index += 1
        if index == len(Tele.participants):
            return
        for participant in Tele.participants:
            Tele.bot.send_message(participant.identifier, f"{Tele.participants[index].name} покинул беседу")
        Tele.bot.reply_to(message, "Вы покинули беседу.")
        Tele.employer.delete_person(Tele.participants[index].name)
        name__ = Tele.participants[index].name
        Tele.participants.pop(index)
        if len(Tele.participants) == 0:
            exit()
        who, reply = Tele.employer.say_first_sentence()
        for participant_num in range(len(Tele.participants)):
            participant = Tele.participants[participant_num]
            if participant.identifier != message.chat.id:
                Tele.bot.send_message(participant.identifier, f"{name__}: {message.text}")
            Tele.bot.send_message(Tele.participants[participant_num].identifier, text=f"Сообщение для {who}: {reply}")

    @staticmethod
    @bot.message_handler(func=lambda message: True)
    def _echo_all(message):
        if message.from_user.is_bot:
            return

        index = 0
        while index < len(Tele.participants) and Tele.participants[index].identifier != message.chat.id:
            index += 1
        if index == len(Tele.participants):
            return
        who, reply = Tele.employer.answer_on_message(Tele.participants[index].name, message.text)
        for participant_num in range(len(Tele.participants)):
            participant = Tele.participants[participant_num]
            if participant.identifier != message.chat.id:
                Tele.bot.send_message(participant.identifier, f"{Tele.participants[index].name}: {message.text}")
            Tele.bot.send_message(Tele.participants[participant_num].identifier, text=f"Сообщение для {who}: {reply}")

    @staticmethod
    def start_polling():
        Tele.bot.polling()
