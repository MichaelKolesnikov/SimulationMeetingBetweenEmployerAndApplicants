import math
import re
import numpy as np
import openai
import gpt_settings


def extract_numbers(reply: str) -> list[float]:
    return list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", reply)))


def calculate_the_share_of_each_intention(intentions: dict[int, str], gpt_model_name: str, fraze: str) -> list[float]:
    cat_str = ', '.join(intentions.values())
    num = len(intentions.values())
    completion = openai.chat.completions.create(
        model=gpt_model_name,
        messages=[
            {
                "role": "assistant",
                "content": gpt_settings.Prompts.get_prompt_for_determining_intentions(num, cat_str, fraze)
            }
        ]
    )
    return extract_numbers(completion.choices[0].message.content)


def generate_answer(last_message, messages, model, prev_scheme, current_scheme):
    changed_message = gpt_settings.Prompts.get_changed_message(last_message)

    if current_scheme - prev_scheme == 0 and current_scheme == 1:
        changed_message = gpt_settings.Prompts.current_stage_1 + changed_message
    elif current_scheme - prev_scheme == 0 and current_scheme == 2:
        changed_message = gpt_settings.Prompts.current_stage_2 + changed_message
    elif current_scheme - prev_scheme == 0 and current_scheme == 3:
        changed_message = gpt_settings.Prompts.current_stage_3 + changed_message
    if current_scheme - prev_scheme == 1 and current_scheme == 2:
        changed_message = gpt_settings.Prompts.from1to2 + changed_message
    if current_scheme - prev_scheme == 1 and current_scheme == 3:
        changed_message = gpt_settings.Prompts.from2to3 + changed_message

    messages_opt = list(messages)
    messages_opt.append({"role": "user", "content": changed_message})

    completion = openai.chat.completions.create(model=model, messages=messages_opt)
    reply_ans = completion.choices[0].message.content
    return reply_ans


def get_distance(point1, point2):
    return math.sqrt(sum((a_i - b_i) ** 2 for a_i, b_i in zip(point1, point2)))


def list_of_list_to_str(list_):
    string = ''
    for sublist in list_:
        for elem in sublist:
            string = string + str(elem) + ' '
        string = string + ','
    return string


def list_to_str(list_):
    string = ''
    for elem in list_:
        string = string + str(elem) + ' '
    return string


def who_is_on_the_duty_today(persons):
    scores = []
    for i in range(len(persons)):
        moral = persons[i].schemes.count(True)
        dist = persons[i].current_dist()
        score = (moral + 1) * 2 - dist
        scores.append(score)
    total = sum(scores)
    normalized_scores = [x / total for x in scores]
    selected_number = np.random.choice(len(normalized_scores), p=normalized_scores)
    return selected_number
