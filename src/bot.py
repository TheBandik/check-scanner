from aiogram import types

import telebot

import settings
import scanner
import db


bot = telebot.TeleBot(settings.bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    db.add_user(user_id)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.chat.id
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.photo[1].file_id + '.png'
        with open(src, 'wb') as f:
            f.write(downloaded_file)
        bot.reply_to(message, 'Изображение получено')
    except Exception as e:
        bot.reply_to(message, e)
    
    products = scanner.scan(user_id, src)
    if type(products) == list:
        text = ''
        for product in products:
            text += f'{product}\n\n'
        bot.send_message(user_id, text, parse_mode=types.ParseMode.HTML)
    elif products == '0':
        bot.send_message(user_id, 'Ошибка. Получить данные по этому чеку невозможно')
    elif products == '1':
        bot.send_message(user_id, 'Распознать QR-код не удалось, попробуйте еще раз')

print('bot is working')
bot.infinity_polling()
