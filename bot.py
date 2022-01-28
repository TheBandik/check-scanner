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
        bot.reply_to(message, 'Получено')
    except Exception as e:
        bot.reply_to(message, e)
    
    scanner.scan(user_id, src)

print('bot is working')
bot.infinity_polling()
