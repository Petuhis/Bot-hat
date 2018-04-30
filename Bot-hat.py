from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup
from random import choice

all_words = ['Прыть', 'Аперитив', 'Изверг', 'Кириллица', 'Добавка', 'Пора', 'Династия', 'Суперсила', 'Брехня',
             'Консистенция', 'Адресат', 'Консилиум', 'Проводник', 'Прадед', 'Обучение', 'Пленение', 'Баламут', 'Сговор',
             'Ребрендинг', 'Среда обитания', 'Фриланс', 'Артефакт', 'Республиканец', 'Добытчик', 'Маньяк', 'Пример',
             'Зло', 'Малахит', 'Пакля,конспирация', 'Контингент', 'Ребрендинг', 'Беспредельщик',
             'Деверь/золовка (и прочая родня)', 'Отношение', 'Невидаль', 'Плешь', 'Утопия', 'Адмиралтейство', 'Пора',
             'Пустомеля', 'Брехня', 'Ветошь', 'Шпрехшталмейстер', 'Википедия',
             'Дилижанс', 'Отрочество', 'Проказник', 'Категория', 'Вид', 'Неряха', 'Бремя', 'Стыд', 'Звонница',
             'Обращение', 'Позывной', 'Коллапс', 'Загагулина', 'Муть', 'Бяка/бука,инерция', 'Проказа', 'Эксклюзив',
             'Диктатор', 'Карапулька', 'Меломан', 'Игротека', 'Целесообразность', 'Воротила', 'Бит-боксер', 'Казус',
             'Намёк', 'Чебупели', 'Восхождение', 'Новаторство', 'Материк', 'Катаклизм', 'Энциклопедия', 'Доблесть',
             'Ассоциация', 'Организация', 'Выдумка', 'Пустозвон', 'Юриспруденция', 'Полонез', 'Реформа', 'Порка',
             'Куча', 'Контингент', 'Инфраструктура', 'Косяк', 'Кара', 'Каракатица', 'Мелиорация', 'Стёб', 'Мангуст',
             'Стерильность', 'Амбиции', 'Блиц', 'Фальш', 'Сваха', 'Фисташка', 'Антураж', 'Жмот', 'Выемка', 'Шлепок',
             'Инкассатор', 'Репертуар', 'Отшельник', 'Лунтик', 'Гоп-стоп', 'Бельмо', 'Энергия', 'Минимализм',
             'Воздействие', 'Покровитель', 'Амёба', 'Захват', 'Миролюбие', 'Ресурс', 'Феерия', 'Сутолока', 'Зарево',
             'Коронация', 'Язь (рыба моей мечты)', 'Ультрафиолет', 'Падчерица', 'Тыколка', 'Хмырь', 'Ширпотреб',
             'Тарабарщина', 'Глюкометр', 'Тёзка', 'Поверие', 'Принцип', 'Паж', 'Сруб', 'Обожествление', 'Нестыковка',
             'Трапеза', 'Отношение', 'Экстрасенс', 'Анонс', 'Экспромт', 'Концепция', 'Негодование', 'Престиж', 'Шоумен']

const_size_for_round = 10
start_keyboard = [['Угадано'],
                  ['Поехали'],
                  ['Cформировать новый список слов']]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)


def start(bot, update, chat_data):
    update.message.reply_text('Я бот-шляпа.\n'
                              'В начале игры формируется список слов. Игра заключается в том, чтобы '
                              '"вытаскивать" слова из "шляпы", после чего объяснять их значения, не используя однокоренные слова. '
                              'Каждая команда ограничена 1 минутой, в течение которого она может '
                              'продолжать вытаскивать слова. По истечении этого времени "шляпа" передается другой '
                              'команде. Всего 2 команды.', reply_markup=start_markup)
    chat_data['team_1'] = 0
    chat_data['team_2'] = 0
    chat_data['current_team'] = True
    chat_data['words'] = []
    chat_data['current_word'] = 0
    chat_data['round'] = 1


def generator(chat_data):
    chat_data['words'] = []
    for i in range(const_size_for_round):
        random_word = choice(all_words)
        while random_word in chat_data['words']:
            random_word = choice(all_words)
        chat_data['words'].append(random_word)
    chat_data['current_word'] = 0
    return chat_data


def text_analyzer(bot, update, job_queue, chat_data):
    if chat_data == {}:
        chat_data['team_1'] = 0
        chat_data['team_2'] = 0
        chat_data['current_team'] = True
        chat_data['words'] = []
        chat_data['current_word'] = 0
        chat_data['round'] = 1

    if update.message.text == 'Поехали':
        if len(chat_data['words']) != const_size_for_round:
            chat_data = generator(chat_data)
        chat_data['current_word'] = 0
        start_round(bot, update, job_queue, chat_data)

    elif update.message.text == 'Cформировать новый список слов':
        chat_data = generator(chat_data)
        update.message.reply_text('Список слов сформирован.')

    elif update.message.text == 'Угадано':
        if chat_data['current_word'] + 1 < len(chat_data['words']):
            chat_data['current_word'] += 1

            if chat_data['current_team']:
                chat_data['team_1'] += 1
            else:
                chat_data['team_2'] += 1
            update.message.reply_text("Угадано {0} из {1}".format(chat_data["current_word"], len(chat_data["words"])))

            update.message.reply_text(chat_data['words'][chat_data['current_word']])

        else:
            if 'job' in chat_data:
                chat_data['job'].schedule_removal()
                del chat_data['job']
            chat_data['round'] += 1
            if chat_data['round'] > 3:
                if chat_data['team_1'] > chat_data['team_2']:
                    update.message.reply_text('Первая команда победила!')
                elif chat_data['team_2'] > chat_data['team_1']:
                    update.message.reply_text('Вторая команда победила!')
                else:
                    update.message.reply_text('Ничья!')
            else:
                chat_data = generator(chat_data)
                update.message.reply_text('Рауд {} начнется по нажатию кнопки "Поехали".'.format(chat_data['round']))
                if chat_data['current_team']:
                    update.message.reply_text('Приготовиться первой команде.')
                else:
                    update.message.reply_text('Приготовиться второй команде.')


def task(bot, job):
    job.context[1]["current_team"] = not job.context[1]["current_team"]
    if job.context[1]["current_team"]:
        bot.send_message(job.context[0], text="Ход первой команды.")
    else:
        bot.send_message(job.context[0], text="Ход второй команды.")

    bot.send_message(job.context[0], text=job.context[1]["words"][job.context[1]["current_word"]])


def start_round(bot, update, job_queue, chat_data):
    delay = 60
    job = job_queue.run_repeating(task, delay, context=[update.message.chat_id, chat_data])
    chat_data['job'] = job
    round = chat_data['round']
    update.message.reply_text('Раунд {}!'.format(round))
    update.message.reply_text(chat_data["words"][chat_data["current_word"]])


def main():
    token = '576442066:AAHLVST3fXd_U_G9hLOkXJDHq4mbj0ro0_A'
    request_kwargs = {'proxy_url': 'https://192.116.142.153:8080'}
    updater = Updater(token, request_kwargs=request_kwargs)
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, text_analyzer, pass_chat_data=True, pass_job_queue=True)
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start, pass_chat_data=True))
    dp.add_handler(CommandHandler("task", task, pass_chat_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
