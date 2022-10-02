import pymysql

import settings


# Подключение к БД
db = pymysql.connect(
    host=settings.host,
    port=settings.port,
    user=settings.user,
    password=settings.password,
    db=settings.db,
    charset=settings.charset
)
cursor = db.cursor()

# Добавление пользователя
def add_user(user_id):
    # Создание таблицы пользователей, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS users(' +
        'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
        'tel_id INTEGER NOT NULL' +
        ')')
    db.commit()

    # Проверка на налачие пользователя в БД
    cursor.execute(f'SELECT tel_id FROM users WHERE tel_id = {user_id}')
    data = cursor.fetchone()
    # Если пользователя нет, то он добавляется в БД
    if data is None:
        cursor.execute(f'INSERT INTO users(tel_id) VALUES({user_id})')
        db.commit()

# Добавление чека
def add_receipt(tel_id, receipt):
    # Создание таблицы чеков, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS receipts(' +
        'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
        'receipt TEXT NOT NULL,' +
        'user_id INTEGER NOT NULL,' +
        'FOREIGN KEY (user_id) REFERENCES users (id)' +
        ')')
    db.commit()

    # Получение user_id
    cursor.execute(f"SELECT id FROM users WHERE tel_id = {tel_id}")
    user_id = cursor.fetchone()[0]

    # Проверка на налачие чека в БД
    cursor.execute(f"SELECT receipt FROM receipts WHERE receipt = '{receipt}'")
    data = cursor.fetchone()
    # Если чека нет, то он добавляется в БД
    if data is None:
        cursor.execute(f"INSERT INTO receipts(receipt, user_id) VALUES('{receipt}', {user_id})")
        db.commit()

# Получение списка категорий
def get_categories():
    # Получение списка категорий нижнего уровня
    cursor.execute('select id, name, tags from categories where tags is not null')
    categories = cursor.fetchall()
    
    return categories
