import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic import *
from datetime import datetime

TELEGRAM_TOKEN = '6712865092:AAHubde1HD3RkAM-DeP32DR-V4aEL1onSQ4'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Регистрация потеряшки", callback_data="reg_lost"),
                               InlineKeyboardButton("Просмотр потеряшек", callback_data="see_lost"))
    return markup



def gen_getitem(items):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    for item in items:
        markup.add(InlineKeyboardButton(item[0], callback_data=f"item_{item[0]}"),
                   )
    return markup



def date_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("3 дня", callback_data="last3"),
                               InlineKeyboardButton("неделя", callback_data="lastweek"), 
                               InlineKeyboardButton("За всё время", callback_data="alltime")),
    
    return markup






@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "reg_lost":
        bot.send_message(call.message.chat.id, "Введите название вещи:")
        bot.register_next_step_handler(call.message, reg_step1)

    elif call.data == "see_lost":
        res = manager.get_items()
        for i in range(len(res[::4])):
            s = ""
            paths = []
            for item in res[i*4:(i+1)*4]:
                paths.append(item[3])
                s += f"{item[0]}. {item[1]}\n{item[2]}\n\n"
            bot.send_message(call.message.chat.id, s,reply_markup=gen_getitem(res))
            manager.collage_creation(paths, "output.png")
            img = open("output.png", 'rb')
            bot.send_photo(call.message.chat.id, img)

    elif call.data.startswith("item"):
        item_id = call.data.split("_")[1]
        item_info = manager.get_items_data(item_id)
        print(item_info)
        bot.send_message(call.message.chat.id, f"{item_info[0][1]}\n")
        img = item_info[0][3]
        img = open(img, 'rb')
        bot.send_photo(call.message.chat.id, img)
        #bot.send_message(call.message.chat.id, s.split(",")[1] + "\n" + s.split(",")[3]) #почему-то F строки не работали



        



        



        #bot.send_message(call.message.chat.id, "Выбери временной период в который ты потерял свою вещь" ,reply_markup=date_markup())

def reg_step1(message):
    name = message.text
    bot.send_message(message.chat.id, "Отправьте фото вещи:")
    bot.register_next_step_handler(message, photo, name=name)



def photo(message,name):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    rightnow = datetime.now()

    with open(f"img/{message.id}.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    manager.add_items(name,f"img/{message.id}.jpg",rightnow)
    bot.send_message(message.chat.id, "Вещь добавлена в список потеряшек")


@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "ㅤ", reply_markup=gen_markup())

if __name__ == "__main__":
    manager = StoreManager(DATABASE)


    bot.infinity_polling()
