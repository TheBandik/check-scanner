import aiogram

import telebot

import settings
import scanner
import db
import categorization


# Подключение к боту по токену
bot = telebot.TeleBot(settings.bot_token)
db.create_db()

# Команда start
@bot.message_handler(commands=['start'])
def start(message):
    # Получение id пользователя
    user_id = message.chat.id
    # Добавление id пользователя в базу
    db.add_user(user_id)

# Получение изображения
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Получение id пользователя
    user_id = message.chat.id
    try:
        # Получение информации об изображении
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        # Загрузка изображения
        downloaded_file = bot.download_file(file_info.file_path)
        # Добавление расширения для изображения
        src = message.photo[1].file_id + '.png'
        # Сохранение изображения
        with open(src, 'wb') as f:
            f.write(downloaded_file)
        bot.reply_to(message, 'Изображение получено, ожидайте получение чека...')
    except Exception as e:
        bot.reply_to(message, e)
    
    # Запуск сканирования QR-кода
    products = scanner.scan(user_id, src)
    # Проверка списка товаров
    if type(products) == list:
        # Формирование и отправка сообщения со списком товаров
        text = ''
        for product in products:
            text += f'{product}\n\n'
            # Определение категории товара
            categorization.category_detection(product)
        bot.send_message(user_id, text, parse_mode=aiogram.types.ParseMode.HTML)
    elif products == '0':
        bot.send_message(user_id, 'Ошибка. Получить данные по этому чеку невозможно')
    elif products == '1':
        bot.send_message(user_id, 'Распознать QR-код не удалось, попробуйте еще раз')


# Дебаг
print('bot is working')
# Работа бота
bot.infinity_polling()
