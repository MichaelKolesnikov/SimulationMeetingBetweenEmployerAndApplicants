import re
from olympiad_data_structures.PointVector import PointVector
import gpt_settings
import description_of_spaces
import openai


def extract_numbers(reply: str) -> list[float]:
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", reply)
    return [float(num) for num in numbers]


class ManagementOfIntentionalities:
    @staticmethod
    def calculate_the_share_of_each_intention(
            intentions: dict[int, str],
            gpt_model_name: str, fraze: str) -> list[float]:
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

    @staticmethod
    def generate_answer(
            last_message,
            messages,
            gpt_model_name: str,
            prev_scheme,
            current_scheme) -> str | None:
        changed_message = gpt_settings.Prompts.get_changed_message(last_message)

        if current_scheme - prev_scheme == 1 and current_scheme == 2:
            changed_message = gpt_settings.Prompts.from1to2 + changed_message
        elif current_scheme - prev_scheme == 1 and current_scheme == 3:
            changed_message = gpt_settings.Prompts.from2to3 + changed_message

        messages_opt = list(messages)
        messages_opt.append({"role": "user", "content": changed_message})

        completion = openai.chat.completions.create(model=gpt_model_name, messages=messages_opt)
        return completion.choices[0].message.content

    @staticmethod
    def test_moral():
        appraisals: list[list[float]] = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0]]
        feelings = [[0, 0.5, 0.5, 0.6, 0.6], [0.6, 0.6, 0.4, 0.6, 0.2], [0.3, 0.3, 0.3, 0.4]]

        schemes = [False, False, False]

        current_scheme = 1
        messages = [{"role": "assistant", "content": gpt_settings.Prompts.start_prompt}]

        r1 = gpt_settings.forgetting_factor
        r2 = gpt_settings.forgetting_factor_for_feelings

        while True:
            message = input("User : ")
            print(f'Сх: {schemes}')
            action = ManagementOfIntentionalities.calculate_the_share_of_each_intention(description_of_spaces.spaces[current_scheme - 1], "gpt-3.5-turbo", message)
            for i in range(len([current_scheme - 1])):
                appraisals[current_scheme - 1][i] = (1 - r1) * appraisals[current_scheme - 1][i] + r1 * action[i]
            dist = PointVector(*appraisals[current_scheme - 1]).distance(PointVector(*feelings[current_scheme - 1]))
            prev_scheme = current_scheme
            if dist > 0.25:
                for i in range(len(appraisals[current_scheme - 1])):
                    feelings[current_scheme - 1][i] = (1 - r2) * feelings[current_scheme - 1][i] + r2 * (appraisals[current_scheme - 1][i] - feelings[current_scheme - 1][i])
            else:
                schemes[current_scheme - 1] = True
                current_scheme = min(current_scheme + 1, 3)
            reply = ManagementOfIntentionalities.generate_answer(
                message,
                messages,
                gpt_settings.model_name,
                prev_scheme,
                current_scheme
            )
            print(f"Objective parameters:{appraisals[current_scheme - 1]}")
            print(f"Subjective parameters:{feelings[current_scheme - 1]}")
            print(f"Distance:{dist}")
            for i in range(len(appraisals[current_scheme - 1])):
                appraisals[current_scheme - 1][i] = (1 - r1) * appraisals[current_scheme - 1][i] + r1 * 0.3 * feelings[current_scheme - 1][i]

            print(f"ChatGPT: {reply}")
            messages.append({"role": "user", "content": message})
            messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    ManagementOfIntentionalities.test_moral()
