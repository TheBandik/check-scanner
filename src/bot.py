import aiogram
import asyncio

import telebot

import settings
import scanner
import db


# Подключение к боту по токену
bot = telebot.TeleBot(settings.bot_token)

# Отправка рассылки
def send_notify(msg, users, user_id):
    # Рассылка сообщения всем пользователям
    if msg.text == '0':
        bot.send_message(user_id, 'Рассылка отменена')
    else:
        for user in users:
            bot.send_message(user[0], msg.text)

# Команда start
@bot.message_handler(commands=['start'])
def start(message):
    # Получение id пользователя
    user_id = message.chat.id
    # Добавление id пользователя в базу
    asyncio.run(db.DataBase.add_user(user_id, bot))

# Команда about
@bot.message_handler(commands=['about'])
def about(message):
    # Получение id пользователя
    user_id = message.chat.id
    # Текущая версия
    version = 'pre-alpha'
    # Отправка сообщения пользователю
    bot.send_message(user_id, f'К разработке бота приложили лапки: @thebandik\n@ellismi\n\nТекущая версия: {version}')

# Команда notify (знают о ней только админы)
@bot.message_handler(commands=['notify'])
def notify(message):
    # Получение id пользователя
    user_id = message.chat.id
    # Получение id всех пользователей
    users = asyncio.run(db.DataBase.get_users())
    if (user_id, 1) in users:
        # Получение сообщения для рассылки
        msg = bot.send_message(user_id, 'Отправьте в чат текст для рассылки. Для отмены отправьте цифру 0')
        bot.register_next_step_handler(msg, send_notify, users, user_id)
    else:
        bot.send_message(user_id, 'Команда доступна только администраторам')

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
    products = scanner.scan(user_id, src, bot)
    
    # Проверка списка товаров
    if type(products) == list:
        # Формирование и отправка сообщения со списком товаров
        text = ''
        for product in products:
            text += f'{product}\n\n'
        bot.send_message(user_id, 'Товары распределены по категориям')
        bot.send_message(user_id, text, parse_mode=aiogram.types.ParseMode.HTML)
    elif products == '0':
        bot.send_message(user_id, 'Ошибка. Получить данные по этому чеку невозможно')
    elif products == '1':
        bot.send_message(user_id, 'Распознать QR-код не удалось, попробуйте еще раз')


# Дебаг
print('bot is working')
# Работа бота
bot.infinity_polling()
