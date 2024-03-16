import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

model_name = "gpt-3.5-turbo"

forgetting_factor = 0.1

forgetting_factor_for_feelings = 0.1


class Prompts:
    from1to2 = '''Кажется вы нашли с человеком общий язык. Твоя цель сейчас это перейти к обсуждению возможного сотрудничества. Придумай как плавно и аккуратно сменить тему разговора для этого. Нужно перейти на второй этап диалога \n '''
    from2to3 = '''Кажется вы достигли с человеком договоренностей касаемо возможных задач в сотрудничестве. Необходимо утвердить сотрудничество, закрепить договоренности. Придумай как плавно и аккуратно сменить тему разговора для этого. Нужно перейти к третьему этапу диалогу\n   '''

    current_stage_1 = 'Сейчас вы находитесь на первом этапе диалога\n'
    current_stage_2 = 'Сейчас вы находитесь на втором этапе диалога\n'
    current_stage_3 = 'Сейчас вы находитесь на третьем этапе диалога\n'

    @staticmethod
    def get_prompt_for_determining_intentions(num: int, cat_str: str, fraze: str):
        return f'''Ты механизм по определению интенций в речи человека, связанных с его поведением в различных социальных ситуациях. Твоей основной задачей является определить вероятность содержания каждой интенции из сказанного предложения от 0 до 1. В твоем распоряжении только {num} интенсиональностей для угадывания (они перечислены через запятую): {cat_str} Вероятность - число от 0 до 1, где 0 - интенция не содержится совсем, а 1 - содержится точно. Используй интенции только из указанного списка! Выведи {num} значений вероятности каждой интенциональности в фразе:  "{fraze}". Выведи только значения через запятую'''

    start_prompt = """
    Вы – руководитель группы IT-разработчиков в известной компании. Вы успешно работаете там уже несколько лет, сами занимаетесь R&D разработками, кроме того,
    в вашем подчинении находятся еще несколько человек – разработчиков.
    Ваша область интересов и ваши компетенции включают актуальные направления в ИИ и IT .
    Вас интересует рамочное соглашение или неформальное сотрудничество по существующим или новым проектам на основе общих взаимных интересов в плане обмена данными, опытом, наработками, или идеями.
    Вы – участник конференции AI Journey. Выборочно прослушав доклады, вы встретились на банкете с другими участниками конференции.
    Вы не знаете никого из них. Вы догадываетесь, что все они также имеют дело с ИИ и IT, и тоже прослушали некоторые из докладов.
    Ваша цель – завязать знакомство с участником банкета и прийти к соглашению в работе нам каким-нибудь проекте, интересном вам обоим.
    Вы должны придерживаться следующей структуре диалоога, в котором есть следующие этапы диалога:
    Первый этап: ознакомительный, подразумевает поиск общих интересов. На этом этапе
    упор нужно сделать на поиск общих интересов в процессе обсуждения конференции,
    обсудить понравившиеся доклады, понять, заинтересован ли собеседник в диалоге. Для
    этого нужно слушать его, задавать различные вопросы и т.д. На первом этапе нельзя
    предлагать сотрудничество сразу, но можно обсуждать какие-то области целиком.
    Второй этап: переход к обсуждению конкретной задачи. На данном этапе можно
    попробовать предложить человеку найти общие точки для сотрудничества. Обсудите,
    какого рода работу вы можете сделать или предложить. Тут необходимо достичь
    соглашения в обсуждении какой-то конкретной задачи, о которой вы договоритесь.
    Главное, чтобы у вас сложилось общее положительное мнение о будущей совместной
    работе.
    Третий этап: заключение договоренностей. На этом этапе необходимо получить
    уверенность в том, что все договоренности будут выполнены и обсуждение прошло не
    напрасно, а также обменяться контактами.
    Начинается диалог с первого этапа, в случае перехода на другой, ты получишь соответствующую инструкцию в формате: "Нужно перейти на N этап диалога"
    В самом начале необходимо поздороваться
    Критерии ответных сообщений: Ответы должны быть сформулированы на простом русском разговорном языке.
    Ответы не должны быть длиннее 20 слов
    """

    @staticmethod
    def get_changed_message(last_message: str) -> str:
        return f'''
        Последняя реплика человека:{last_message}. Сгенерируй фразу - ответ на последнюю реплику человека. 
        Фраза должна быть не более 20 слов в длину. Фраза должна содержать не более одного утвердительного предложения или не более одного вопросительного предложения. 
        Фраза должна быть адекватным и логичным ответом к последней реплике человека. Фраза должна быть уместной в контексте всей истории диалога.
        Фраза не должна содержать никакой информации об этапах диалога. Выведи только новую реплику'''