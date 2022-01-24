from email import message
import telebot

import settings


bot = telebot.TeleBot(settings.bot_token)

@bot.message_handler(commands=['test'])
def test_message(message):
    bot.send_message(message.chat.id, 'Тест')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'images/' + message.photo[1].file_id + '.jpg'
        with open(src, 'wb') as f:
            f.write(downloaded_file)
        bot.reply_to(message, 'Я сохраню это')
    except Exception as e:
        bot.reply_to(message, e)

print('bot is working')
bot.infinity_polling()
