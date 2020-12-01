import telebot
import time
import json
import os

from telebot import types
from datetime import datetime, date, timedelta

token = os.environ.get('bot_token')
bot = telebot.TeleBot(str(token))
print('Бот работает!')

data_loads = json.load(open('./schedule.json'))
data = json.dumps(data_loads)
json_data = json.loads(data)

data_loads1 = json.load(open('./users.json'))
data1 = json.dumps(data_loads1)
json_data1 = json.loads(data1)

@bot.message_handler(commands = ['update'])
def update_sender(message):
    users_get = json_data1["users"]
    values = 0
    for x in users_get:
        bot.send_message(users_get[values], "Бот обновился до v1.2\n"
                                            "\n*Коротко* о новом обновлении:" 
                                            "\n• Появилась функция отмены для команды «Оставить пожелание»;"
                                            "\n• В расписании рядом с днём теперь стоит дата."
                                            "\n\nИ также небольшой вопрос - интересно ли Вам получать краткую сводку об обновлениях (выходит раз в неделю)? Если да - пишите в «Оставить пожелание» слово «Да», если нет, то напишите «Нет»", parse_mode = 'Markdown')
        values += 1
@bot.message_handler(commands = ['start'])
def start_command(message):
    str_countes = ''
    countes = [f'{message.from_user.id} - ID,\n',
               f'{message.from_user.first_name} - имя,\n',
               f'{message.from_user.last_name} - фамилия,\n',
               f'{message.from_user.username} - username.'
              ]
    for x in countes:
        str_countes += x
    bot.send_message(655041562, f'У тебя +1 новый пользователь! \n{str_countes}')
    bot.reply_to(message, "Рад тебя видеть! Пропиши /schedule!")
@bot.message_handler(commands = ['help'])
def send_help(message):
    bot.reply_to(message, "Привет! Рад, что ты заглянул(а) сюда :) \n1) /schedule - узнать расписание")
@bot.message_handler(commands = ['schedule'])
def schedule(message):
    delta = timedelta(hours = 3)
    now = datetime.now() + delta
    days_int = now.isoweekday()
    sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
    d1 = sep - timedelta(days = sep.weekday())
    d2 = now - timedelta(days = now.weekday())
    parity = ((d2 - d1).days // 7) % 2 #возвращает 0, если неделя нечётная и 1, если чётная
    
    if parity == 0:
        schedule_days_int = json_data["Для нечётной недели"]
        schedule = ''
        for x in schedule_days_int:
            keys = schedule_days_int.get(str(days_int))
        nowtime = now.strftime("(%d.%m.%y)")
        schedule += str(keys)
        schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.add(button, button1)
        bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        schedule_days_int = json_data["Для чётной недели"]
        schedule = ''
        for x in schedule_days_int:
            keys = schedule_days_int.get(str(days_int))
        nowtime = now.strftime("(%d.%m.%y)")
        schedule += str(keys)
        schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.add(button, button1)
        bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
@bot.message_handler(content_types = ['text'])
def text(message):
    if message.text == 'Расписание на сегодня':
        delta = timedelta(hours = 3)
        now = datetime.now() + delta
        days_int = now.isoweekday()
        sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
        d1 = sep - timedelta(days = sep.weekday())
        d2 = now - timedelta(days = now.weekday())
        parity = ((d2 - d1).days // 7) % 2 #возвращает 0, если неделя нечётная и 1, если чётная
        
        if parity == 0:
            schedule_days_int = json_data["Для нечётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_int))
            nowtime = now.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Оставить пожелание")
            keyboard.add(button, button1)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        else:
            schedule_days_int = json_data["Для чётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_int))
            nowtime = now.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Оставить пожелание")
            keyboard.add(button, button1)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'Оставить пожелание':
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Отмена")
        keyboard.add(button)
        bot.send_message(message.chat.id, "Напиши своё сообщение, а я отправлю его разработчику, \nлибо отправь «Отмена» для отмены!", reply_markup = keyboard)
        bot.register_next_step_handler(message, get_message)
def get_message(message):
    callback = message.text
    if callback == "Отмена" or callback == "отмена":
        bot.clear_step_handler_by_chat_id(chat_id = message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.add(button, button1)
        bot.send_message(message.chat.id, "Готово!", parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.add(button, button1)
        bot.send_message(message.chat.id, "Готово! Спасибо за отзыв!", reply_markup = keyboard)
        bot.send_message(655041562, f'Кто-то оставил фидбэк: \n*{callback}*', parse_mode = 'Markdown', reply_markup = keyboard)
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as e:
            time.sleep(3)
            print(f'Возникла ошибка: {e}')
