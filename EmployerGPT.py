from functions import *
from Person import Person


class EmployerGPT:
    def __init__(self, names: list[str], start_messages: list[str], logging_file_name: str = 'logs1and2.txt'):
        self.appraisals: list[list[float]] = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0]]
        self.feelings = [[0, 0.45, 0.45, 0.5, 0.5], [0.4, 0.4, 0.4, 0.3, 0.2], [0.3, 0.3, 0.3, 0.4]]
        self.logging_file_name = logging_file_name
        self.schemes = [False, False, False]

        self.messages = [{"role": "assistant", "content": gpt_settings.Prompts.start_prompt}]
        self.n = len(start_messages)
        self.persons: list[Person] = []
        self.persons_deleted = []
        for i in range(self.n):
            self.persons.append(Person(1, 1, self.appraisals, self.feelings, self.schemes, self.messages, names[i]))
        for i in range(self.n):
            self.write(f"{self.persons[i].name}:" + start_messages[i] + '\n')
            self.persons[i].action_effect(start_messages[i])

    def say_first_sentence(self) -> tuple[str, str]:
        who = who_is_on_the_duty_today(self.persons)
        reply = self.persons[who].make_reply()
        self.write(f"Бот - обращение к {self.persons[who].name}: {reply}" + '\n')
        return self.persons[who].name, reply

    def write(self, some_string: str):
        with open(self.logging_file_name, 'a', encoding='utf-8') as f:
            f.write(some_string)

    def answer_on_message(self, who_name: str, message: str) -> tuple[str, str] | None:
        for i in range(len(self.persons)):
            if self.persons[i].name == who_name:
                who = i
                break
        else:
            print("Name is not in names")
            return None

        self.write(f"{self.persons[who].name} : " + message + '\n')

        self.persons[who].action_effect(message)
        self.write('Appr:' + list_of_list_to_str(self.persons[who].appr) + '\n')
        self.write('Feelings:' + list_of_list_to_str(self.persons[who].feelings) + '\n')
        self.write('Schemes:' + list_to_str(self.persons[who].schemes) + '\n')
        self.write('Dist:' + str(self.persons[who].current_dist()) + '\n')

        who = who_is_on_the_duty_today(self.persons)
        reply = self.persons[who].make_reply()
        self.write(f"Бот - обращение к {self.persons[who].name}: {reply} \n")

        return self.persons[who].name, reply

    def delete_person(self, person_name: str) -> None:
        for i in range(len(self.persons)):
            if self.persons[i].name == person_name:
                self.persons.pop(i)
                break


def main():
    employer = EmployerGPT(["Michael", "Jake"], ["Здравствуйте", "Добрый день!"], "log.txt")
    who, reply = employer.say_first_sentence()
    while True:
        print(reply)
        mes = input(f"{who}: ")
        who, reply = employer.answer_on_message(who, mes)


if __name__ == "__main__":
    main()
