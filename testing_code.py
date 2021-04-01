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

data_loads6 = json.load(open('./rating.json'))
data6 = json.dumps(data_loads6)
json_data6 = json.loads(data6)


rating = json_data4["Список"]
percents = json_data4["Проценты"]
id_groups = json_data6["id_groups"]

sorted_dict = {}
sorted_keys = sorted(percents, key = percents.get, reverse = True)
for w in sorted_keys:
    sorted_dict[w] = percents[w]
layout = ''
layout_id = ''
layout_percents = ''
key = 0

for x, y in zip(rating, percents):
    surname = rating.get(str(key))
    percent_cources = percents.get(str(key))
    key += 1
    layout += f'{surname} — {percent_cources}%\n'
    
for key, value in id_groups.items():
    surname = rating.get(str(key))
    id_ = id_groups.get(str(key))
    layout_id += f'{surname} — id: `{id_}`\n'
    
for key, value in sorted_dict.items():
    surname = f'{value}%'
    percent_cources = rating.get(str(key))
    layout_percents += f'{percent_cources} — {surname}\n'  

message_password = os.environ.get('pwd')
message_password_email = os.environ.get('pwd_mail')

message_physics = """ 
*Физика*
• Курсы:
├ https://bit.ly/2ZvQKsJ (teach-in);
└ https://bit.ly/3jYshWt (youtube)
• Иные полезные материалы:
└ https://clck.ru/TTQ2L (google drive)
"""

message_math = """
*Математический анализ*
• Курсы:
└ https://bit.ly/2OLpbtb (youtube)
"""

message_english = """
*Английский язык*
• Учебники:
├ https://bit.ly/3pxRvfs — первая группа;
└ https://bit.ly/3ayKEhD — вторая группа
"""

page_list = 1
url_lists_eng = f"""
*Английский язык*
• Поиск по страницам"""

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
                if schedule == '':
                    schedule = "Упс, но ты ввёл что-то не так."
                bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)   
        except:
            bot.send_message(message.chat.id, 'Так. Тут что-то не так. \nВведи числа (от 1 до 7), либо обратись к @whomet.')

@bot.message_handler(commands = ['buildings'])
def buildings(message):
    keyboard = types.InlineKeyboardMarkup()
    buildings_1 = types.InlineKeyboardButton(text = "1️⃣ Первый корпус", callback_data = 'adress_1')
    buildings_2 = types.InlineKeyboardButton(text = "2️⃣ Второй корпус", callback_data = 'adress_2')
    buildings_3 = types.InlineKeyboardButton(text = "3️⃣ Третий корпус", callback_data = 'adress_3')
    buildings_4 = types.InlineKeyboardButton(text = "4️⃣ Четвёртый корпус", callback_data = 'adress_4')
    buildings_5  = types.InlineKeyboardButton(text = "5️⃣ ККМТ", callback_data = 'adress_5')
    buildings_6  = types.InlineKeyboardButton(text = "5️⃣ Спортзал", callback_data = 'adress_6')
    url_button = types.InlineKeyboardButton(text = "Открыть интерактивную карту ↗️", url = 'https://bit.ly/3fl8EY6')
    keyboard.row(buildings_1, buildings_2, buildings_3)
    keyboard.row(buildings_4, buildings_5, buildings_6)
    keyboard.row(url_button)
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
            button = types.InlineKeyboardButton(text = "🆎 Сортировка по фамилиям", callback_data = 'family')
            button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню", callback_data = 'back_to_the_menu')
            keyboard.row(button)
            keyboard.row(button1)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f'*Рейтинг по курсу, сортировка по* _процентам_. \n\n{layout_percents}', parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'family':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "💯 Сортировка по процентам", callback_data = 'percent')
            button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню", callback_data = 'back_to_the_menu')
            keyboard.row(button)
            keyboard.row(button1)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f'*Рейтинг по курсу, сортировка по* _фамилиям_. \n\n{layout}', parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'delete':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
            bot.delete_message(call.message.chat.id, call.message.message_id - 2)
        elif call.data == 'delete_pwd':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        
        elif call.data == 'useful_materials':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "Физика", callback_data = 'physics')
            button1 = types.InlineKeyboardButton(text = "Английский язык", callback_data = 'english')
            button3 = types.InlineKeyboardButton(text = "Мат. анализ", callback_data = 'mat_analysis')
            button2 = types.InlineKeyboardButton(text = "⬅️ Назад в меню", callback_data = 'back_to_the_menu')
            keyboard.row(button, button1)
            keyboard.row(button3, button2) 
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '🧠 *Полезные материалы.*', parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'physics':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "⬅️ Назад в полезные материалы", callback_data = 'useful_materials')
            keyboard.row(button)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message_physics, parse_mode = 'Markdown', reply_markup = keyboard)
        elif call.data == 'english':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "⬅️ Назад в полезные материалы", callback_data = 'useful_materials')
            keyboard.row(button)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message_english, parse_mode = 'Markdown', reply_markup = keyboard)
        elif call.data == 'required_page':
            global page_list
            page_list = 1
            keyboard = types.InlineKeyboardMarkup()
            button_page1 = types.InlineKeyboardButton(text = f"Страница {page_list + 1}", callback_data = 'page')
            button_page2 = types.InlineKeyboardButton(text = f"Страница {page_list + 2}", callback_data = 'next_page')
            button1 = types.InlineKeyboardButton(text = "Вперёд", callback_data = 'further')
            button = types.InlineKeyboardButton(text = "⬅️ Назад в материалы по английскому языку", callback_data = 'english')
            keyboard.row(button_page1, button_page2, button1)
            keyboard.row(button)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = url_lists_eng, parse_mode = 'Markdown', reply_markup = keyboard)
        elif call.data == 'further':
            page_list += 1
            keyboard = types.InlineKeyboardMarkup()
            button_page1 = types.InlineKeyboardButton(text = f"Страница {page_list + 1}", callback_data = f'page{page_list + 1}')
            button_page2 = types.InlineKeyboardButton(text = f"Страница {page_list + 2}", callback_data = f'next_page{page_list + 2}')
            button1 = types.InlineKeyboardButton(text = "Вперёд", callback_data = 'further')
            button = types.InlineKeyboardButton(text = "⬅️ Назад в материалы по английскому языку", callback_data = 'english')
            keyboard.row(button_page1, button_page2, button1)
            keyboard.row(button)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = url_lists_eng, parse_mode = 'Markdown', reply_markup = keyboard)
        elif call.data == f'page{page_list + 1}' or call.data == f'next_page{page_list + 2}':
            msg = f"""
            https://studfile.net/preview/5753521/page:{page_list}/ — первая группа;
            https://studfile.net/preview/5753537/page:{page_list}/ — вторая группа
            """
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "⬅️ Назад в материалы по английскому языку", callback_data = 'english')
            keyboard.row(button)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = msg, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'mat_analysis':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "⬅️ Назад в полезные материалы", callback_data = 'useful_materials')
            keyboard.row(button)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message_math, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'passwords':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "Для локальной сети", callback_data = 'local')
            button1 = types.InlineKeyboardButton(text = "Для тестирования", callback_data = 'testing')
            button3 = types.InlineKeyboardButton(text = "Для почты", callback_data = 'mail')
            button4 = types.InlineKeyboardButton(text = "⬅️ Назад в меню", callback_data = 'back_to_the_menu')
            keyboard.row(button, button1)
            keyboard.row(button3, button4)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '📋 *Меню паролей.*', parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'local':
            keyboard = types.InlineKeyboardMarkup()
            delete = types.InlineKeyboardButton(text = "⬅️ Назад в меню паролей", callback_data = 'passwords')
            keyboard.add(delete)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message_password, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'mail':
            keyboard = types.InlineKeyboardMarkup()
            delete = types.InlineKeyboardButton(text = "⬅️ Назад в меню паролей", callback_data = 'passwords')
            keyboard.add(delete)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message_password_email, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'testing':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "⬅️ Назад в меню паролей", callback_data = 'cancel')
            button1 = types.InlineKeyboardButton(text = "❔ Узнать ID", callback_data = 'find_out_the_ID')
            keyboard.row(button1, button)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '💬 *Напиши свой ID*. \n\nЕсли же ты его _не знаешь_, или _забыл_, обратись к пункту меню «Узнать ID», нажав на соответствующую кнопку.', parse_mode = 'Markdown', reply_markup = keyboard)
            bot.register_next_step_handler(call.message, get_message)
        
        elif call.data == 'find_out_the_ID':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "⬅️ Назад в меню паролей", callback_data = 'cancel')
            keyboard.add(button)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f'{layout_id}\n*Отлично!* \nА теперь смело вводи ID.', parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'cancel':
            bot.clear_step_handler_by_chat_id(chat_id = call.message.chat.id)
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "Для локальной сети", callback_data = 'local')
            button1 = types.InlineKeyboardButton(text = "Для тестирования", callback_data = 'testing')
            button3 = types.InlineKeyboardButton(text = "Для почты", callback_data = 'mail')
            button4 = types.InlineKeyboardButton(text = "⬅️ Назад в меню", callback_data = 'back_to_the_menu')
            keyboard.row(button, button1)
            keyboard.row(button3, button4)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '📋 *Меню паролей.*', parse_mode = 'Markdown', reply_markup = keyboard)
            
        elif call.data == 'back_to_the_menu':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "Полезные материалы", callback_data = 'useful_materials')
            button2 = types.InlineKeyboardButton(text = "Рейтинг по курсу", callback_data = 'rating_by_course')
            button4 = types.InlineKeyboardButton(text = "Пароли", callback_data = 'passwords')
            button5 = types.InlineKeyboardButton(text = "Расписание по датам", callback_data = 'schedule_by_date')
            keyboard.row(button)
            keyboard.row(button2)
            keyboard.row(button4)
            keyboard.row(button5)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '📜 *Главное меню.*', parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'schedule_by_date':
            delta = timedelta(hours = 3)
            delta1 = timedelta(days = 1)
            delta2 = timedelta(days = 2)
            delta3 = timedelta(days = 3)
            delta4 = timedelta(days = 4)
            now_next = datetime.now() + delta + delta1
            now_next1 = datetime.now() + delta + delta2
            now_next2 = datetime.now() + delta + delta3
            now_next3 = datetime.now() + delta + delta4
            now_next = now_next.strftime("%d.%m.%y")
            now_next1 = now_next1.strftime("%d.%m.%y")
            now_next2 = now_next2.strftime("%d.%m.%y")
            now_next3 = now_next3.strftime("%d.%m.%y")
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = f"{now_next}", callback_data = 'now_next')
            button1 = types.InlineKeyboardButton(text = f"{now_next1}", callback_data = 'now_next1')
            button2 = types.InlineKeyboardButton(text = f"{now_next2}", callback_data = 'now_next2')
            button3 = types.InlineKeyboardButton(text = f"{now_next3}", callback_data = 'now_next3')
            url_button = types.InlineKeyboardButton(text = f"Открыть полное расписание ↗️", url = 'https://bit.ly/3cxSxEV')
            button4 = types.InlineKeyboardButton(text = f"⬅️ Назад в меню", callback_data = 'back_to_the_menu')
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            keyboard.row(url_button)
            keyboard.row(button4)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f'🗓 *Расписание по датам (бета, может работать не совсем правильно).*', parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'now_next3':
            delta = timedelta(hours = 3)
            delta1 = timedelta(days = 3)
            delta2 = timedelta(days = 4)
            now = datetime.now() + delta
            now_next = datetime.now() + delta + delta1
            nowtime = datetime.now() + delta + delta2
            days_int = now_next.isoweekday()
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
                nowtime = nowtime.strftime("(%d.%m.%y)")
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню расписаний", callback_data = 'schedule_by_date')
                keyboard.row(button1)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = schedule, parse_mode = 'Markdown', reply_markup = keyboard)
            else:
                schedule_days_int = json_data3["Для чётной недели"]
                schedule = ''
                for x in schedule_days_int:
                    keys = schedule_days_int.get(str(days_print))
                nowtime = nowtime.strftime("(%d.%m.%y)")
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню расписаний", callback_data = 'schedule_by_date')
                keyboard.row(button1)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'now_next2':
            delta = timedelta(hours = 3)
            delta1 = timedelta(days = 2)
            delta2 = timedelta(days = 3)
            now = datetime.now() + delta
            now_next = datetime.now() + delta + delta1
            nowtime = datetime.now() + delta + delta2
            days_int = now_next.isoweekday()
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
                nowtime = nowtime.strftime("(%d.%m.%y)")
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню расписаний", callback_data = 'schedule_by_date')
                keyboard.row(button1)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = schedule, parse_mode = 'Markdown', reply_markup = keyboard)
            else:
                schedule_days_int = json_data3["Для чётной недели"]
                schedule = ''
                for x in schedule_days_int:
                    keys = schedule_days_int.get(str(days_print))
                nowtime = nowtime.strftime("(%d.%m.%y)")
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню расписаний", callback_data = 'schedule_by_date')
                keyboard.row(button1)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'now_next1':
            delta = timedelta(hours = 3)
            delta1 = timedelta(days = 1)
            delta2 = timedelta(days = 2)
            now = datetime.now() + delta
            now_next = datetime.now() + delta + delta1
            nowtime = datetime.now() + delta + delta2
            days_int = now_next.isoweekday()
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
                nowtime = nowtime.strftime("(%d.%m.%y)")
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню расписаний", callback_data = 'schedule_by_date')
                keyboard.row(button1)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = schedule, parse_mode = 'Markdown', reply_markup = keyboard)
            else:
                schedule_days_int = json_data3["Для чётной недели"]
                schedule = ''
                for x in schedule_days_int:
                    keys = schedule_days_int.get(str(days_print))
                nowtime = nowtime.strftime("(%d.%m.%y)")
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню расписаний", callback_data = 'schedule_by_date')
                keyboard.row(button1)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'now_next':
            delta = timedelta(hours = 3)
            delta1 = timedelta(days = 1)
            now = datetime.now() + delta
            now_next = datetime.now() + delta
            nowtime = datetime.now() + delta + delta1
            days_int = now_next.isoweekday()
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
                nowtime = nowtime.strftime("(%d.%m.%y)")
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню расписаний", callback_data = 'schedule_by_date')
                keyboard.row(button1)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = schedule, parse_mode = 'Markdown', reply_markup = keyboard)
            else:
                schedule_days_int = json_data3["Для чётной недели"]
                schedule = ''
                for x in schedule_days_int:
                    keys = schedule_days_int.get(str(days_print))
                nowtime = nowtime.strftime("(%d.%m.%y)")
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню расписаний", callback_data = 'schedule_by_date')
                keyboard.row(button1)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        
        elif call.data == 'rating_by_course':
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text = "💯 Сортировка по процентам", callback_data = 'percent')
            button1 = types.InlineKeyboardButton(text = "⬅️ Назад в меню", callback_data = 'back_to_the_menu')
            keyboard.row(button)
            keyboard.row(button1)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f'*Рейтинг по курсу, сортировка по* _фамилиям_. \n\n{layout}', parse_mode = 'Markdown', reply_markup = keyboard)
        
        
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
        buildings_1 = types.InlineKeyboardButton(text = "1️⃣ Первый корпус", callback_data = 'adress_1')
        buildings_2 = types.InlineKeyboardButton(text = "2️⃣ Второй корпус", callback_data = 'adress_2')
        buildings_3 = types.InlineKeyboardButton(text = "3️⃣ Третий корпус", callback_data = 'adress_3')
        buildings_4 = types.InlineKeyboardButton(text = "4️⃣ Четвёртый корпус", callback_data = 'adress_4')
        buildings_5  = types.InlineKeyboardButton(text = "5️⃣ ККМТ", callback_data = 'adress_5')
        buildings_6  = types.InlineKeyboardButton(text = "6️⃣ Спортзал", callback_data = 'adress_6')
        url_button = types.InlineKeyboardButton(text = "Открыть интерактивную карту ↗️", url = 'https://bit.ly/3fl8EY6')
        keyboard.row(buildings_1, buildings_2, buildings_3)
        keyboard.row(buildings_4, buildings_5, buildings_6)
        keyboard.row(url_button)
        photo = open('./Buildings/buildings.png', 'rb')
        bot.send_photo(message.chat.id, photo, reply_markup = keyboard)
    elif message.text == 'Меню':
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text = "Полезные материалы", callback_data = 'useful_materials')
        button2 = types.InlineKeyboardButton(text = "Рейтинг по курсу", callback_data = 'rating_by_course')
        button4 = types.InlineKeyboardButton(text = "Пароли", callback_data = 'passwords')
        button5 = types.InlineKeyboardButton(text = "Расписание по датам", callback_data = 'schedule_by_date')
        keyboard.row(button)
        keyboard.row(button2)
        keyboard.row(button4)
        keyboard.row(button5)
        bot.send_message(message.chat.id, '📜 *Главное меню.*', parse_mode = 'Markdown', reply_markup = keyboard)
    #подобие ИИ
    elif re.search(r'\bпривет', message.text.lower()):
        with open ('./AI/hello.txt', 'r') as file:
            lines = file.readlines()
        bot.send_message(message.chat.id, random.choice(lines))
    
def get_message(message):
    id = message.text
    if id.isdigit() == False or int(id) > 30:
        bot.clear_step_handler_by_chat_id(chat_id = message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text = "Для локальной сети", callback_data = 'local')
        button1 = types.InlineKeyboardButton(text = "Для тестирования", callback_data = 'testing')
        button3 = types.InlineKeyboardButton(text = "Для почты", callback_data = 'mail')
        button4 = types.InlineKeyboardButton(text = "⬅️ Назад в меню", callback_data = 'back_to_the_menu')
        keyboard.row(button, button1)
        keyboard.row(button3, button4)
        bot.send_message(message.chat.id, "Введён неправильный/несуществующий ID, Вы были возвращены в *меню паролей.*", parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text = "⬅️ Назад в меню паролей", callback_data = 'passwords')
        url_button = types.InlineKeyboardButton(text = "Перейти на сайт тестирования ↗️", url = 'https://do.unitech-mo.ru')
        keyboard.row(url_button)
        keyboard.row(button)
        bot.send_message(message.chat.id, f"{json_data5['id'][id]['name']}, лови свои логин и пароль! \n\n*Логин:* `{json_data5['id'][id]['login']}` \n*Пароль:* `{json_data5['id'][id]['pass']}`", parse_mode = 'Markdown', reply_markup = keyboard)
        
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as e:
            time.sleep(3)
            print(f'Возникла ошибка: {e}')
