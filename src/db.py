import sqlite3


# Подключение к БД
connect = sqlite3.connect('products.db', check_same_thread=False)
cursor = connect.cursor()

# Добавление пользователя
def add_user(user_id):
    # Создание таблицы пользователей, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS users(' +
        'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,' +
        'tel_id INTEGER NOT NULL' +
        ')')
    connect.commit()

    # Проверка на налачие пользователя в БД
    cursor.execute(f'SELECT tel_id FROM users WHERE tel_id = {user_id}')
    data = cursor.fetchone()
    # Если пользователя нет, то он добавляется в БД
    if data is None:
        cursor.execute(f'INSERT INTO users(tel_id) VALUES({user_id})')
        connect.commit()

# Добавление чека
def add_receipt(user_id, receipt):
    # Создание таблицы чеков, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS receipts(' +
        'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,' +
        'receipt TEXT NOT NULL,' +
        'user_id INTEGER NOT NULL,' +
        'FOREIGN KEY (user_id) REFERENCES users(id)' +
        ')')
    connect.commit()

    # Проверка на налачие чека в БД
    cursor.execute(f"SELECT receipt FROM receipts WHERE receipt = '{receipt}'")
    data = cursor.fetchone()
    # Если чека нет, то он добавляется в БД
    if data is None:
        cursor.execute(f"INSERT INTO receipts(receipt, user_id) VALUES('{receipt}', {user_id})")
        connect.commit()
