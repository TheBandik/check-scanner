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
    # Проверка на налачие пользователя в БД
    cursor.execute(f'SELECT telegram_id FROM users WHERE telegram_id = {user_id}')
    data = cursor.fetchone()
    # Если пользователя нет, то он добавляется в БД
    if data is None:
        cursor.execute(f'INSERT INTO users(telegram_id) VALUES({user_id})')
        db.commit()

# Добавление чека
def add_receipt(telegram_id, receipt, store, date):
    # Получение user_id
    cursor.execute(f"SELECT id FROM users WHERE telegram_id = {telegram_id}")
    user_id = cursor.fetchone()[0]

    # Получение store_id
    cursor.execute(f"SELECT id FROM stores WHERE name = '{store}'")
    store_id = cursor.fetchone()[0]

    # Проверка на налачие чека в БД
    cursor.execute(f"SELECT receipt FROM receipts WHERE receipt = '{receipt}'")
    data = cursor.fetchone()
    # Если чека нет, то он добавляется в БД
    if data is None:
        cursor.execute(f"INSERT INTO receipts(receipt, date, user_id, store_id) VALUES('{receipt}', '{date}', {user_id}, {store_id})")
        db.commit()

# Добавление магазина
def add_store(store_name, store_address):
    # Проверка на налачие магазина в БД
    cursor.execute(f"SELECT name FROM stores WHERE name = '{store_name}'")
    data = cursor.fetchone()
    # Если магазина нет, то он добавляется в БД
    if data is None:
        cursor.execute(f"INSERT INTO stores(name, address) VALUES('{store_name}', '{store_address}')")
        db.commit()

# Добавление имени товара
def add_product_name(product_name):
    # Проверка на налачие имени товара в БД
    cursor.execute(f"SELECT name FROM product_names WHERE name = '{product_name}'")
    data = cursor.fetchone()
    # Если имени товара нет, то он добавляется в БД
    if data is None:
        cursor.execute(f"INSERT INTO product_names(name) VALUES('{product_name}')")
        db.commit()

# Добавление товара
def add_product(product_name, receipt, sum, quantity, vat, vat_sum, price, category_id):
    # Получение product_name_id
    cursor.execute(f"SELECT id FROM product_names WHERE name = '{product_name}'")
    product_name_id = cursor.fetchone()[0]

    # Получение product_name_id
    cursor.execute(f"SELECT id FROM receipts WHERE receipt = '{receipt}'")
    receipt_id = cursor.fetchone()[0]

    # Добавление товара в БД
    cursor.execute(f"INSERT INTO products(product_name_id, sum, quantity, vat, vat_sum, price, receipt_id, category_id)" +
        f"VALUES({product_name_id}, {sum}, {quantity}, {vat}, {vat_sum}, {price}, {receipt_id}, {category_id})")
    db.commit()

# Получение списка категорий
def get_categories():
    # Получение списка категорий нижнего уровня
    cursor.execute('select id, name, tags from categories where tags is not null')
    categories = cursor.fetchall()
    
    return categories

def create_db():
    # Создание таблицы пользователей, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS users(' +
        'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
        'telegram_id INTEGER NOT NULL,' +
        'role INTEGER DEFAULT 0' +
        ')')
    db.commit()

    # Создание таблицы магазинов, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS stores(' +
        'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
        'name VARCHAR(255),' +
        'address VARCHAR(255)' +
        ')')
    db.commit()

    # Создание таблицы чеков, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS receipts(' +
        'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
        'receipt TEXT NOT NULL,' +
        'date VARCHAR(255) NOT NULL,' +
        'user_id INTEGER NOT NULL,' +
        'store_id INTEGER NOT NULL,' +
        'FOREIGN KEY (user_id) REFERENCES users (id),' +
        'FOREIGN KEY (store_id) REFERENCES stores (id)' +
        ')')
    db.commit()

    # Создание таблицы наименования товаров, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS product_names(' +
        'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
        'name VARCHAR(255)' +
        ')')
    db.commit()

    # Создание таблицы категорий, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS categories(' +
        'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
        'name VARCHAR(255),' +
        'tags TEXT,' +
        'category_id INTEGER DEFAULT NULL,' +
        'FOREIGN KEY (category_id) REFERENCES categories (id),' +
        'UNIQUE (name)' +
        ')')
    db.commit()

    # Создание таблицы товаров, если её нет
    cursor.execute('CREATE TABLE IF NOT EXISTS products(' +
        'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
        'product_name_id INTEGER NOT NULL,' +
        'sum FLOAT,' +
        'quantity FLOAT,' +
        'vat TINYINT,' +
        'vat_sum FLOAT,' +
        'price FLOAT,' +
        'receipt_id INTEGER NOT NULL,' +
        'category_id INTEGER NOT NULL,' +
        'FOREIGN KEY (receipt_id) REFERENCES receipts (id),' +
        'FOREIGN KEY (category_id) REFERENCES categories (id),' +
        'FOREIGN KEY (product_name_id) REFERENCES product_names (id)' +
        ')')
    db.commit()
