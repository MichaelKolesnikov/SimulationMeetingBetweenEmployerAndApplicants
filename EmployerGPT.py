from functions import *
from Person import Person


class EmployerGPT:
    def __init__(self, start_messages: list[str], logging_file_name: str = 'logs.txt'):
        self.appraisals: list[list[float]] = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0]]
        self.feelings = [[0, 0.5, 0.5, 0.6, 0.6], [0.6, 0.6, 0.4, 0.6, 0.2], [0.3, 0.3, 0.3, 0.4]]
        self.logging_file_name = logging_file_name
        self.schemes = [False, False, False]

        self.messages = [{"role": "assistant", "content": gpt_settings.Prompts.start_prompt}]
        self.n = len(start_messages)
        self.persons: list[Person] = []
        self.persons_deleted = []
        for i in range(self.n):
            self.persons.append(Person(1, 1, self.appraisals, self.feelings, self.schemes, self.messages))
        for i in range(self.n):
            self.write(f"{i}:" + start_messages[i] + '\n')
            self.persons[i].action_effect(start_messages[i])

    def say_first_sentence(self) -> tuple[int, str]:
        who = who_is_on_the_duty_today(self.persons)
        reply = self.persons[who].make_reply()
        self.write(f"Бот - обращение к {who}: {reply}" + '\n')
        return who, reply

    def write(self, some_string: str):
        with open(self.logging_file_name, 'a') as f:
            f.write(some_string)

    def answer_on_message(self, person_number: int, message: str) -> tuple[int, str]:
        self.write(f"{person_number} : " + message + '\n')

        self.persons[person_number].action_effect(message)
        self.write('Appr: ' + list_of_list_to_str(self.persons[person_number].appr) + '\n')
        self.write('Feelings: ' + list_of_list_to_str(self.persons[person_number].feelings) + '\n')
        self.write('Schemes: ' + list_to_str(self.persons[person_number].schemes) + '\n')
        self.write('Dist: ' + str(self.persons[person_number].current_dist()) + '\n')

        person_number = who_is_on_the_duty_today(self.persons)
        reply = self.persons[person_number].make_reply()
        self.write(f"Бот - обращение к {person_number}: {reply} \n")

        return person_number, reply

    def delete_person(self, person_number: int) -> None:
        self.persons.pop(person_number)


def main():
    employer = EmployerGPT(["Здравствуйте", "Добрый день!"], "lol.txt")
    who, reply = employer.say_first_sentence()
    while True:
        print(reply)
        mes = input(f"{who}: ")
        who, reply = employer.answer_on_message(who, mes)


if __name__ == "__main__":
    main()
