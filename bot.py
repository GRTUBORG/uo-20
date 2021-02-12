import telebot
import time
import json
import os

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
    bot.send_message(655041562, f'У тебя +1 новый пользователь! \n{str_countes}')
    bot.reply_to(message, "Рад тебя видеть! Пропиши /schedule! Если вдруг ты заблудился или забыл команды (со всеми бывает, не переживай) — /help в помощь.")

    
@bot.message_handler(commands = ['update'])
def update_sender(message):
    users_get = json_data1["users"]
    video = open('./1.7/1.7.mp4', 'rb')
    values = 0
    for x in users_get:
        bot.send_message(users_get[values], "Бот обновился до v1.7 (12.02.21)\n"
                                            "\n*Коротко* о новом обновлении:" 
                                            "\n• Всё смотри в видео ниже!"
                                            "\n• В случае возникновения/выявления багов/ошибок/косяков — просьба незамедлительно писать в форму «Оставить пожелание»", parse_mode = 'Markdown')
        bot.send_video(users_get[values], video) 
        values += 1


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
            keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Оставить пожелание")
            keyboard.add(button, button1, button2)
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
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Оставить пожелание")
            keyboard.add(button, button1, button2)
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
                keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
                button = types.KeyboardButton(text = "Расписание на сегодня")
                button1 = types.KeyboardButton(text = "Расписание на завтра")
                button2 = types.KeyboardButton(text = "Оставить пожелание")
                keyboard.add(button, button1, button2)
                bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
            else:
                schedule_days_int = json_data["Для чётной недели"]
                schedule = ''
                for x in schedule_days_int:
                    keys = schedule_days_int.get(message.text[10:])
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', 'для этой недели')
                keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
                button = types.KeyboardButton(text = "Расписание на сегодня")
                button1 = types.KeyboardButton(text = "Расписание на завтра")
                button2 = types.KeyboardButton(text = "Оставить пожелание")
                keyboard.add(button, button1, button2)
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
    keyboard.add(buildings_1, buildings_2, buildings_3, buildings_4)
    photo = open('./Buildings/buildings.png', 'rb')
    bot.send_photo(message.chat.id, photo, reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'adress_1':
            bot.send_message(call.message.chat.id, 'Первый корпус. \n*улица Гагарина, 42*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.916027, 37.819657)
        elif call.data == 'adress_2':
            bot.send_message(call.message.chat.id, 'Второй корпус. \n*Октябрьская улица, 10А*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.918151, 37.811716)
        elif call.data == 'adress_3':
            bot.send_message(call.message.chat.id, 'Третий корпус. \n*Пионерская улица, 19А*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.914358, 37.809803)
        elif call.data == 'adress_4':
            bot.send_message(call.message.chat.id, 'Четвёртый корпус. \n*Октябрьский бульвар, 12*', parse_mode = 'Markdown')
            bot.send_location(call.message.chat.id, 55.916840, 37.829620)

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
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Расписание на завтра")
        button2 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.add(button, button1, button2)
        bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        schedule_days_int = json_data3["Для чётной недели"]
        schedule = ''
        for x in schedule_days_int:
            keys = schedule_days_int.get(str(days_print))
        nowtime = now_next.strftime("(%d.%m.%y)")
        schedule += str(keys)
        schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Расписание на завтра")
        button2 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.add(button, button1, button2)
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
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Оставить пожелание")
            keyboard.add(button, button1, button2)
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
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Оставить пожелание")
            keyboard.add(button, button1, button2)
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
            keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Оставить пожелание")
            keyboard.add(button, button1, button2)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        else:
            schedule_days_int = json_data3["Для чётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_print))
            nowtime = now_next.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "Оставить пожелание")
            keyboard.add(button, button1, button2)
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
        button1 = types.KeyboardButton(text = "Расписание на завтра")
        button2 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.add(button, button1, button2)
        bot.send_message(message.chat.id, "Готово, отменил отправку! \nВоспользуйся клавиатурой ниже, чтобы узнать актуальное расписание.", parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        str_countes = ''
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Расписание на завтра")
        button2 = types.KeyboardButton(text = "Оставить пожелание")
        keyboard.add(button, button1, button2)
        bot.send_message(message.chat.id, "Готово! Спасибо за отзыв!", reply_markup = keyboard)
        countes = [f'{message.from_user.id} — ID,\n',
                   f'{message.from_user.first_name} — имя,\n',
                   f'{message.from_user.last_name} — фамилия,\n',
                   f'{message.from_user.username} — username.'
                  ]
        for x in countes:
            str_countes += x
        bot.send_message(655041562, f'• *Кто-то оставил фидбэк:* \n«{callback}» \n\n• *Прилетел от:* \n{str_countes}', parse_mode = 'Markdown', reply_markup = keyboard)

        
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as e:
            time.sleep(3)
            print(f'Возникла ошибка: {e}')
