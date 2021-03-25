import telebot
import time
import json
import os
import re
import random

from telebot import types
from datetime import datetime, date, timedelta


token = os.environ.get('bot_token')
bot = telebot.TeleBot(str(token))
print('Бот работает!')

days_count = ['1', '2', '3', '4', '5', '6', '7']

data_loads = json.load(open('./schedule.json'))
data = json.dumps(data_loads)
json_data = json.loads(data)

data_loads1 = json.load(open('./users.json'))
data1 = json.dumps(data_loads1)
json_data1 = json.loads(data1)

data_loads3 = json.load(open('./schedule_next_day.json'))
data3 = json.dumps(data_loads3)
json_data3 = json.loads(data3)

data_loads4 = json.load(open('./rating.json'))
data4 = json.dumps(data_loads4)
json_data4 = json.loads(data4)

data_loads5 = json.load(open('./pwd_tests.json'))
data5 = json.dumps(data_loads5)
json_data5 = json.loads(data5)

rating = json_data4["Список"]
percents = json_data4["Проценты"]
sorted_dict = {}
sorted_keys = sorted(percents, key = percents.get, reverse = True)
for w in sorted_keys:
    sorted_dict[w] = percents[w]
layout = ''
layout_percents = ''
key = 0
for x, y in zip(rating, percents):
    surname = rating.get(str(key))
    percent_cources = percents.get(str(key))
    key += 1
    layout += f'{surname} {percent_cources}%\n'
for key, value in sorted_dict.items():
    surname = f'{value}%'
    percent_cources = rating.get(str(key))
    layout_percents += f'{percent_cources} {surname}\n'  

message_password = os.environ.get('pwd')
message_password_email = os.environ.get('pwd_mail')

message_physics = """ 
• Курсы:
├ https://bit.ly/2ZvQKsJ (teach-in);
└ https://bit.ly/3jYshWt (youtube)

• Иные полезные материалы:
└ https://clck.ru/TTQ2L (google drive)
"""

message_math = """
• Курсы:
└ https://bit.ly/2OLpbtb (youtube)
"""

message_english = """
• Учебники:
├ https://bit.ly/3pxRvfs — первая группа;
└ https://bit.ly/3ayKEhD — вторая группа
"""

@bot.message_handler(commands = ['start'])
def start_command(message):
    str_countes = ''
    countes = [f'{message.from_user.id} — ID,\n',
               f'{message.from_user.first_name} — имя,\n',
               f'{message.from_user.last_name} — фамилия,\n',
               f'{message.from_user.username} — username.'
              ]
    for x in countes:
        str_countes += x
    bot.send_message(767815871, f'У тебя +1 новый пользователь! \n{str_countes}')
    bot.reply_to(message, "Рад тебя видеть! Пропиши /schedule! Если вдруг ты заблудился или забыл команды (со всеми бывает, не переживай) — /help в помощь.")

    
'''@bot.message_handler(commands = ['update'])
def update_sender(message):
    users_get = json_data1["users"]
    values = 0
    for x in users_get:
        bot.send_message(users_get[values], "Бот обновился до v1.7 (12.02.21)\n"
                                            "\n*Коротко* о новом обновлении:" 
                                            "\n• Добавил отправку адресов и местоположений в команде /buildings. Попробуй!"
                                            "\n• В случае возникновения/выявления багов/ошибок/косяков — просьба незамедлительно писать в форму «Оставить пожелание»", parse_mode = 'Markdown')
        values += 1'''


@bot.message_handler(commands = ['help'])
def send_help(message):
    bot.reply_to(message, "Привет! Рад, что ты заглянул(а) сюда \n• /schedule — узнать расписание;"
                                                               "\n• /schedule_next — расписание на завтра;"
                                                               "\n• /schedule [цифра] — расписание для конкретного дня недели;"
                                                               "\n• /buildings — адреса всех корпусов.")


@bot.message_handler(commands = ['schedule'])
def schedule(message):
    if message.text == '/schedule':
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
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Адреса корпусов")
            button3 = types.KeyboardButton(text = "Меню")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        else:
            schedule_days_int = json_data["Для чётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_int))
            nowtime = now.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Адреса корпусов")
            button3 = types.KeyboardButton(text = "Меню")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        try:
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
                    keys = schedule_days_int.get(message.text[10:])
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', 'для этой недели')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
                button = types.KeyboardButton(text = "Расписание на сегодня")
                button1 = types.KeyboardButton(text = "Расписание на завтра")
                button2 = types.KeyboardButton(text = "Адреса корпусов")
                button3 = types.KeyboardButton(text = "Меню")
                keyboard.row(button, button1)
                keyboard.row(button2, button3)
                bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
            else:
                schedule_days_int = json_data["Для чётной недели"]
                schedule = ''
                for x in schedule_days_int:
                    keys = schedule_days_int.get(message.text[10:])
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', 'для этой недели')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
                button = types.KeyboardButton(text = "Расписание на сегодня")
                button1 = types.KeyboardButton(text = "Расписание на завтра")
                button2 = types.KeyboardButton(text = "Адреса корпусов")
                button3 = types.KeyboardButton(text = "Меню")
                keyboard.row(button, button1)
                keyboard.row(button2, button3)
                if schedule == "None":
                    schedule = "Упс, но ты ввёл что-то не так."
                bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)   
        except:
            bot.send_message(message.chat.id, 'Так. Тут что-то не так. Введи числа (от 1 до 7), либо обратись к @whomet!')

@bot.message_handler(commands = ['buildings'])
def buildings(message):
    keyboard = types.InlineKeyboardMarkup()
    buildings_1 = types.InlineKeyboardButton(text = "Первый корпус", callback_data = 'adress_1')
    buildings_2 = types.InlineKeyboardButton(text = "Второй корпус", callback_data = 'adress_2')
    buildings_3 = types.InlineKeyboardButton(text = "Третий корпус", callback_data = 'adress_3')
    buildings_4 = types.InlineKeyboardButton(text = "Четвёртый корпус", callback_data = 'adress_4')
    buildings_5  = types.InlineKeyboardButton(text = "ККМТ", callback_data = 'adress_5')
    buildings_6  = types.InlineKeyboardButton(text = "Спортзал", callback_data = 'adress_6')
    keyboard.add(buildings_1, buildings_2, buildings_3, buildings_4, buildings_5, buildings_6)
    
    photo = open('./Buildings/buildings.png', 'rb')
    bot.send_photo(message.chat.id, photo, reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'adress_1':
            keyboard = types.InlineKeyboardMarkup()
            delete = types.InlineKeyboardButton(text = "Удалить ❌", callback_data = 'delete')
            keyboard.add(delete)
            photo = open('./Buildings/1.png', 'rb')
            bot.send_message(call.message.chat.id, 'Первый корпус. \n*улица Гагарина, 42*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.916027, 37.819657)
            bot.send_photo(call.message.chat.id, photo, reply_markup = keyboard)
        
        elif call.data == 'adress_2':
            keyboard = types.InlineKeyboardMarkup()
            delete = types.InlineKeyboardButton(text = "Удалить ❌", callback_data = 'delete')
            keyboard.add(delete)
            photo = open('./Buildings/2.png', 'rb')
            bot.send_message(call.message.chat.id, 'Второй корпус. \n*Октябрьская улица, 10А*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.918151, 37.811716)
            bot.send_photo(call.message.chat.id, photo, reply_markup = keyboard)
        
        elif call.data == 'adress_3':
            keyboard = types.InlineKeyboardMarkup()
            delete = types.InlineKeyboardButton(text = "Удалить ❌", callback_data = 'delete')
            keyboard.add(delete)
            photo = open('./Buildings/3.png', 'rb')
            bot.send_message(call.message.chat.id, 'Третий корпус. \n*Пионерская улица, 19А*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.914358, 37.809803)
            bot.send_photo(call.message.chat.id, photo, reply_markup = keyboard)
        
        elif call.data == 'adress_4':
            keyboard = types.InlineKeyboardMarkup()
            delete = types.InlineKeyboardButton(text = "Удалить ❌", callback_data = 'delete')
            keyboard.add(delete)
            photo = open('./Buildings/4.png', 'rb')
            bot.send_message(call.message.chat.id, 'Четвёртый корпус. \n*Октябрьский бульвар, 12*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.916840, 37.829620)
            bot.send_photo(call.message.chat.id, photo, reply_markup = keyboard)
        
        elif call.data == 'adress_5':
            keyboard = types.InlineKeyboardMarkup()
            delete = types.InlineKeyboardButton(text = "Удалить ❌", callback_data = 'delete')
            keyboard.add(delete)
            photo = open('./Buildings/5.png', 'rb')
            bot.send_message(call.message.chat.id, 'ККМТ. \n*Пионерская улица, 8*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.913485, 37.813369)
            bot.send_photo(call.message.chat.id, photo, reply_markup = keyboard)
        
        elif call.data == 'adress_6':
            keyboard = types.InlineKeyboardMarkup()
            delete = types.InlineKeyboardButton(text = "Удалить ❌", callback_data = 'delete')
            keyboard.add(delete)
            photo = open('./Buildings/gym.png', 'rb')
            bot.send_message(call.message.chat.id, 'Спортзал. \n*улица Богомолова, 9*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.911603, 37.812318)
            bot.send_photo(call.message.chat.id, photo, reply_markup = keyboard)
        
        elif call.data == 'percent':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "Сортировка по фамилиям", callback_data = 'family')
            keyboard.add(button) 
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = layout_percents, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'family':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "Сортировка по процентам", callback_data = 'percent')
            keyboard.add(button)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = layout, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'delete':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
            bot.delete_message(call.message.chat.id, call.message.message_id - 2)
        elif call.data == 'delete_pwd':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
            
        elif call.data == 'late': 
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message_password, parse_mode = 'Markdown')
            time.sleep(15)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '_Сообщение с паролем было удалено в целях сохранения конфиденциальности._', parse_mode = 'Markdown')
            
@bot.message_handler(commands = ['schedule_next'])
def schedule_next(message):
    delta = timedelta(hours = 3)
    delta1 = timedelta(days = 1)
    now = datetime.now() + delta
    now_next = datetime.now() + delta + delta1
    days_int = now.isoweekday()
    
    sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
    d1 = sep - timedelta(days = sep.weekday())
    d2 = now - timedelta(days = now.weekday())
    parity = ((d2 - d1).days // 7) % 2 #возвращает 0, если неделя нечётная и 1, если чётная
    
    if days_int == 7:
        days_print = 0
        if parity == 0:
            parity = 1
        else:
            parity = 0
    else:
        days_print = days_int
    
        
    if parity == 0:
        schedule_days_int = json_data3["Для нечётной недели"]
        schedule = ''
        for x in schedule_days_int:
            keys = schedule_days_int.get(str(days_print))
        nowtime = now_next.strftime("(%d.%m.%y)")
        schedule += str(keys)
        schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Расписание на завтра")
        button2 = types.KeyboardButton(text = "Адреса корпусов")
        button3 = types.KeyboardButton(text = "Меню")
        keyboard.row(button, button1)
        keyboard.row(button2, button3)
        bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        schedule_days_int = json_data3["Для чётной недели"]
        schedule = ''
        for x in schedule_days_int:
            keys = schedule_days_int.get(str(days_print))
        nowtime = now_next.strftime("(%d.%m.%y)")
        schedule += str(keys)
        schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Расписание на завтра")
        button2 = types.KeyboardButton(text = "Адреса корпусов")
        button3 = types.KeyboardButton(text = "Меню")
        keyboard.row(button, button1)
        keyboard.row(button2, button3)
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
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Адреса корпусов")
            button3 = types.KeyboardButton(text = "Меню")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        else:
            schedule_days_int = json_data["Для чётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_int))
            nowtime = now.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Адреса корпусов")
            button3 = types.KeyboardButton(text = "Меню")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'Расписание на завтра':
        delta = timedelta(hours = 3)
        delta1 = timedelta(days = 1)
        now = datetime.now() + delta
        now_next = datetime.now() + delta + delta1
        days_int = now.isoweekday()
        
        sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
        d1 = sep - timedelta(days = sep.weekday())
        d2 = now - timedelta(days = now.weekday())
        parity = ((d2 - d1).days // 7) % 2 #возвращает 0, если неделя нечётная и 1, если чётная
        
        if days_int == 7:
            days_print = 0
            if parity == 0:
                parity = 1
            else:
                parity = 0
        else:
            days_print = days_int
        
        
        if parity == 0:
            schedule_days_int = json_data3["Для нечётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_print))
            nowtime = now_next.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Адреса корпусов")
            button3 = types.KeyboardButton(text = "Меню")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        else:
            schedule_days_int = json_data3["Для чётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_print))
            nowtime = now_next.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Адреса корпусов")
            button3 = types.KeyboardButton(text = "Меню")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'Адреса корпусов':
        keyboard = types.InlineKeyboardMarkup()
        buildings_1 = types.InlineKeyboardButton(text = "Первый корпус", callback_data = 'adress_1')
        buildings_2 = types.InlineKeyboardButton(text = "Второй корпус", callback_data = 'adress_2')
        buildings_3 = types.InlineKeyboardButton(text = "Третий корпус", callback_data = 'adress_3')
        buildings_4 = types.InlineKeyboardButton(text = "Четвёртый корпус", callback_data = 'adress_4')
        buildings_5  = types.InlineKeyboardButton(text = "ККМТ", callback_data = 'adress_5')
        buildings_6  = types.InlineKeyboardButton(text = "Спортзал", callback_data = 'adress_6')
        keyboard.add(buildings_1, buildings_2, buildings_3, buildings_4, buildings_5, buildings_6)
        photo = open('./Buildings/buildings.png', 'rb')
        bot.send_photo(message.chat.id, photo, reply_markup = keyboard)
    elif message.text == 'Меню':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Полезные материалы")
        button1 = types.KeyboardButton(text = "В меню расписаний")
        button2 = types.KeyboardButton(text = "Рейтинг по курсу")
        button3 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.row(button, button3)
        keyboard.row(button2, button1)
        bot.send_message(message.chat.id, 'Вы перешли в *главное меню*.', parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'Полезные материалы':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Физика")
        button1 = types.KeyboardButton(text = "Английский язык")
        button3 = types.KeyboardButton(text = "Мат. анализ")
        button4 = types.KeyboardButton(text = "Пароли")
        button2 = types.KeyboardButton(text = "В меню расписаний")
        keyboard.row(button, button1)
        keyboard.row(button3, button4)
        keyboard.row(button2)
        bot.send_message(message.chat.id, 'Вы перешли в *полезные материалы*.', parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'Рейтинг по курсу':
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text = "Сортировка по процентам", callback_data = 'percent')
        keyboard.add(button)
        bot.send_message(message.chat.id, layout, parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'Физика':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Физика")
        button1 = types.KeyboardButton(text = "Английский язык")
        button3 = types.KeyboardButton(text = "Мат. анализ")
        button4 = types.KeyboardButton(text = "Пароли")
        button2 = types.KeyboardButton(text = "В меню расписаний")
        keyboard.row(button, button1)
        keyboard.row(button3, button4)
        keyboard.row(button2)
        bot.send_message(message.chat.id, message_physics, reply_markup = keyboard)
    elif message.text == 'Английский язык':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Физика")
        button1 = types.KeyboardButton(text = "Английский язык")
        button3 = types.KeyboardButton(text = "Мат. анализ")
        button4 = types.KeyboardButton(text = "Пароли")
        button2 = types.KeyboardButton(text = "В меню расписаний")
        keyboard.row(button, button1)
        keyboard.row(button3, button4)
        keyboard.row(button2)
        bot.send_message(message.chat.id, message_english, reply_markup = keyboard)
    elif message.text == 'Мат. анализ':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Физика")
        button1 = types.KeyboardButton(text = "Английский язык")
        button3 = types.KeyboardButton(text = "Мат. анализ")
        button4 = types.KeyboardButton(text = "Пароли")
        button2 = types.KeyboardButton(text = "В меню расписаний")
        keyboard.row(button, button1)
        keyboard.row(button3, button4)
        keyboard.row(button2)
        bot.send_message(message.chat.id, message_math, reply_markup = keyboard)
    elif message.text == 'Пароли':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Для локальной сети")
        button1 = types.KeyboardButton(text = "Для тестирования")
        button3 = types.KeyboardButton(text = "Для почты")
        button4 = types.KeyboardButton(text = "В меню расписаний")
        keyboard.row(button, button1)
        keyboard.row(button3, button4)
        bot.send_message(message.chat.id, 'Вы перешли в *меню паролей*', parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'В меню расписаний' or message.text == 'Вернуться назад':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Расписание на завтра")
        button2 = types.KeyboardButton(text = "Адреса корпусов")
        button3 = types.KeyboardButton(text = "Меню")
        keyboard.row(button, button1)
        keyboard.row(button2, button3)
        bot.send_message(message.chat.id, "Вы *вернулись назад* в *меню расписаний*.", parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'Для локальной сети':
        keyboard = types.InlineKeyboardMarkup()
        delete = types.InlineKeyboardButton(text = "Удалить ❌", callback_data = 'delete_pwd')
        keyboard.add(delete)
        bot.send_message(message.chat.id, message_password, parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'Для почты':
        keyboard = types.InlineKeyboardMarkup()
        delete = types.InlineKeyboardButton(text = "Удалить ❌", callback_data = 'delete_pwd')
        keyboard.add(delete)
        bot.send_message(message.chat.id, message_password_email, parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text == 'Оставить пожелание':
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Отмена")
        keyboard.add(button)
        bot.send_message(message.chat.id, "Напиши своё сообщение, а я отправлю его разработчику, \nлибо отправь «Отмена» для отмены!", reply_markup = keyboard)
        bot.register_next_step_handler(message, get_message)
    elif message.text == 'Для тестирования':
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Отмена")
        keyboard.add(button)
        bot.send_message(message.chat.id, 'Напиши свой ID (порядковый номер по журналу). Если же ты его не знаешь, или забыл, обратись к пункту меню "рейтинг по курсу",\nлибо отправь «Отмена» для отмены!', reply_markup = keyboard)
        bot.register_next_step_handler(message, get_pwd_test)
    #подобие ИИ
    elif re.search(r'\bпривет', message.text.lower()):
        with open ('./AI/hello.txt', 'r') as file:
            lines = file.readlines()
        bot.send_message(message.chat.id, random.choice(lines))
    
def get_message(message):
    callback = message.text
    if callback == "Отмена" or callback == "отмена":
        bot.clear_step_handler_by_chat_id(chat_id = message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Полезные материалы")
        button1 = types.KeyboardButton(text = "В меню расписаний")
        button2 = types.KeyboardButton(text = "Рейтинг по курсу")
        button3 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.row(button, button3)
        keyboard.row(button2, button1)
        bot.send_message(message.chat.id, "Готово, отменил отправку и вернул тебя в главное меню.", parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        str_countes = ''
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Полезные материалы")
        button1 = types.KeyboardButton(text = "В меню расписаний")
        button2 = types.KeyboardButton(text = "Рейтинг по курсу")
        button3 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.row(button, button3)
        keyboard.row(button2, button1)
        bot.send_message(message.chat.id, "Готово! Спасибо за отзыв!", reply_markup = keyboard)
        countes = [f'{message.from_user.id} — ID,\n',
                   f'{message.from_user.first_name} — имя,\n',
                   f'{message.from_user.last_name} — фамилия,\n',
                   f'{message.from_user.username} — username.'
                  ]
        for x in countes:
            str_countes += x
        bot.send_message(767815871, f'• *Кто-то оставил фидбэк:* \n{callback} \n\n• *Прилетел от:* \n{str_countes}', parse_mode = 'Markdown', reply_markup = keyboard)
def get_pwd_test(message):
    id = message.text
    if id == "Отмена" or id == "отмена":
        bot.clear_step_handler_by_chat_id(chat_id = message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Для локальной сети")
        button1 = types.KeyboardButton(text = "Для тестирования")
        button3 = types.KeyboardButton(text = "Для почты")
        button4 = types.KeyboardButton(text = "В меню расписаний")
        keyboard.row(button, button1)
        keyboard.row(button3, button4)
        bot.send_message(message.chat.id, "Готово, *отменил* и *вернул* тебя в меню паролей.", parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Для локальной сети")
        button1 = types.KeyboardButton(text = "Для тестирования")
        button3 = types.KeyboardButton(text = "Для почты")
        button4 = types.KeyboardButton(text = "В меню расписаний")
        keyboard.row(button, button1)
        keyboard.row(button3, button4)
        bot.send_message(message.chat.id, f"Держи свои логин и пароль: \n`{json_data5['id'][id]['login']}`\n`{json_data5['id'][id]['pass']}`", parse_mode = 'Markdown', reply_markup = keyboard)
        
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as e:
            time.sleep(3)
            print(f'Возникла ошибка: {e}')
