import copy
from functions import *
from description_of_spaces import *


class Person:
    def __init__(self, prev_scheme, current_scheme, appr, feelings, schemes, dialog, name: str):
        self.prev_scheme = prev_scheme
        self.current_scheme = current_scheme
        self.appr = copy.deepcopy(appr)
        self.feelings = copy.deepcopy(feelings)
        self.schemes = copy.deepcopy(schemes)
        self.dialog = copy.deepcopy(dialog)
        self.last_message: str = ""
        self.name: str = name

    def action_effect(self, message):
        r = gpt_settings.forgetting_factor
        p = gpt_settings.forgetting_factor_for_feelings
        self.last_message = message
        action = calculate_the_share_of_each_intention(spaces_int[self.current_scheme - 1], "gpt-3.5-turbo", message)
        for i in range(len(self.appr[self.current_scheme - 1])):
            self.appr[self.current_scheme - 1][i] = (1 - r) * self.appr[self.current_scheme - 1][i] + r * action[i]
        dist = get_distance(self.appr[self.current_scheme - 1],
                            self.feelings[self.current_scheme - 1])  # расстояния между векторами в текущем пространстве
        self.prev_scheme = self.current_scheme
        if dist > 0.25:  # если превышает пороговое значение
            # Тогда идет перерасчет чувств в текущем пространстве
            for i in range(len(self.appr[self.current_scheme - 1])):
                self.feelings[self.current_scheme - 1][i] = (1 - p) * self.feelings[self.current_scheme - 1][i] + p * (
                        self.appr[self.current_scheme - 1][i] - self.feelings[self.current_scheme - 1][i])
        else:
            # Иначе достигнута моральная схема
            self.schemes[self.current_scheme - 1] = True
            # Переходим к следующей схеме
            self.current_scheme = min(self.current_scheme + 1, 3)  # значение текущей, на которую совершили переход

    def make_reply(self) -> str | None:
        r = gpt_settings.forgetting_factor
        message = self.last_message
        reply = generate_answer(message, self.dialog, "gpt-3.5-turbo", self.prev_scheme, self.current_scheme)
        for i in range(len(self.appr[self.current_scheme - 1])):
            # перерасчет объективных оценок в текущем пространстве посде фразы бота, т..к она тоже влияет на оценку человека, но в меньшей степени
            self.appr[self.current_scheme - 1][i] = (1 - r) * self.appr[self.current_scheme - 1][i] + r * 0.3 * self.feelings[self.current_scheme - 1][i]
        self.dialog.append({"role": "user", "content": message})
        self.dialog.append({"role": "assistant", "content": reply})
        return reply

    def current_dist(self):
        return get_distance(self.appr[self.current_scheme - 1], self.feelings[self.current_scheme - 1])
