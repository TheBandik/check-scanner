import aiomysql

import settings


class DataBase():
    ''' Организация методов для работы с базой данных '''
    @classmethod
    async def connection(self):
        ''' Подключение к базе даннных '''
        self.db = await aiomysql.connect(
            host=settings.host,
            port=settings.port,
            user=settings.user,
            password=settings.password,
            db=settings.db,
            charset=settings.charset,
        )

        self.cursor = await self.db.cursor()

        return True

    @classmethod
    async def add_user(self, user_id, bot):
        ''' Добавление пользователя в базу данных '''
        await self.connection()
        # Проверка на налачие пользователя в БД
        await self.cursor.execute(f'SELECT telegram_id FROM users WHERE telegram_id = {user_id}')
        data = await self.cursor.fetchone()

        # Если пользователя нет, то он добавляется в БД
        if data is None:
            await self.cursor.execute(f'INSERT INTO users(telegram_id) VALUES({user_id})')
            await self.db.commit()

        # Получение telegram_id админов
        await self.cursor.execute(f'SELECT telegram_id FROM users WHERE role = 1')
        admins = await self.cursor.fetchall()

        # Получение информации о новом пользователе
        new_user_info = bot.get_chat_member(data, data).user

        # Отправка админам информации о появлении нового пользователя
        for admin in admins:
            bot.send_message(admin[0], f'У бота появился новый пользователь!\n\nid = {new_user_info.id}\nName = {new_user_info.first_name}\nUsername = {new_user_info.username}')
        
        await self.cursor.close()
        self.db.close()

        return True

    @classmethod
    async def delete_user(self, user_id):
        ''' Удаление пользователя из базы данных '''
        await self.connection()
        # Проверка на налачие пользователя в БД
        await self.cursor.execute(f'SELECT telegram_id FROM users WHERE telegram_id = {user_id}')
        data = await self.cursor.fetchone()
        # Если пользователя есть, то он удалается из БД
        if data:
            await self.cursor.execute(f'DELETE FROM users WHERE telegram_id = {user_id}')
            await self.db.commit()
        
        await self.cursor.close()
        self.db.close()

        return True

    @classmethod
    async def add_store(self, store_name, store_address):
        ''' Добавление магазина в базу данных '''
        await self.connection()
        # Проверка на налачие магазина в БД
        await self.cursor.execute(f"SELECT name FROM stores WHERE name = '{store_name}'")
        data = await self.cursor.fetchone()
        # Если магазина нет, то он добавляется в БД
        if data is None:
            await self.cursor.execute(f"INSERT INTO stores(name, address) VALUES('{store_name}', '{store_address}')")
            await self.db.commit()
        
        await self.cursor.close()
        self.db.close()

        return True

    @classmethod
    async def delete_store(self, store_name, store_address):
        ''' Удаление магазина из базы данных '''
        await self.connection()
        # Проверка на налачие магазина в БД
        await self.cursor.execute(f"SELECT name FROM stores WHERE name = '{store_name}' and address = '{store_address}'")
        data = await self.cursor.fetchone()
        # Если магазин есть, то он удалаяется из БД
        if data:
            await self.cursor.execute(f"DELETE FROM stores WHERE name = '{store_name}' and address = '{store_address}'")
            await self.db.commit()
        
        await self.cursor.close()
        self.db.close()

        return True

    @classmethod
    async def add_receipt(self, telegram_id, receipt, store, date):
        ''' Добавление чека в базу данных '''
        await self.connection()
        # Получение user_id
        await self.cursor.execute(f"SELECT id FROM users WHERE telegram_id = {telegram_id}")
        user_id = await self.cursor.fetchone()

        # Получение store_id
        await self.cursor.execute(f"SELECT id FROM stores WHERE name = '{store}'")
        store_id = await self.cursor.fetchone()

        # Проверка на налачие чека в БД
        await self.cursor.execute(f"SELECT receipt FROM receipts WHERE receipt = '{receipt}'")
        data = await self.cursor.fetchone()
        # Если чека нет, то он добавляется в БД
        if data is None:
            await self.cursor.execute(f"INSERT INTO receipts(receipt, date, user_id, store_id) VALUES('{receipt}', '{date}', {user_id[0]}, {store_id[0]})")
            await self.db.commit()

        await self.cursor.close()
        self.db.close()
    
        return True

    @classmethod
    async def delete_receipt(self, receipt):
        ''' Удаление чека из базы данных '''
        await self.connection()
        # Проверка на налачие чека в БД
        await self.cursor.execute(f"SELECT receipt FROM receipts WHERE receipt = '{receipt}'")
        data = await self.cursor.fetchone()
        # Если чека есть, то он удалается из БД
        if data:
            await self.cursor.execute(f"DELETE FROM receipts WHERE receipt = '{receipt}'")
            await self.db.commit()

        await self.cursor.close()
        self.db.close()
    
        return True

    @classmethod
    async def add_product_name(self, product_name):
        ''' Добавление имени товара в базу данных '''
        await self.connection()
        # Проверка на налачие имени товара в БД
        await self.cursor.execute(f"SELECT name FROM product_names WHERE name = '{product_name}'")
        data = await self.cursor.fetchone()
        # Если имени товара нет, то он добавляется в БД
        if data is None:
            await self.cursor.execute(f"INSERT INTO product_names(name) VALUES('{product_name}')")
            await self.db.commit()

        await self.cursor.close()
        self.db.close()

        return True

    @classmethod
    async def delete_product_name(self, product_name):
        ''' Удаление имени товара из базы данных '''
        await self.connection()
        # Проверка на налачие имени товара в БД
        await self.cursor.execute(f"SELECT name FROM product_names WHERE name = '{product_name}'")
        data = await self.cursor.fetchone()
        # Если именя товара есть, то он удаляется из БД
        if data:
            await self.cursor.execute(f"DELETE FROM product_names WHERE name = '{product_name}'")
            await self.db.commit()

        await self.cursor.close()
        self.db.close()

        return True

    @classmethod
    async def add_product(self, product_name, receipt, sum, quantity, vat, vat_sum, price, category_id):
        ''' Добавление товара в базу данных '''
        await self.connection()
        # Получение product_name_id
        await self.cursor.execute(f"SELECT id FROM product_names WHERE name = '{product_name}'")
        product_name_id = await self.cursor.fetchone()

        # Получение product_name_id
        await self.cursor.execute(f"SELECT id FROM receipts WHERE receipt = '{receipt}'")
        receipt_id = await self.cursor.fetchone()

        # Добавление товара в БД
        await self.cursor.execute(f"INSERT INTO products(product_name_id, sum, quantity, vat, vat_sum, price, receipt_id, category_id)" +
            f"VALUES({product_name_id[0]}, {sum}, {quantity}, {vat}, {vat_sum}, {price}, {receipt_id[0]}, {category_id})")
        await self.db.commit()

        await self.cursor.close()
        self.db.close()

        return True

    @classmethod
    async def delete_product(self, product_name, receipt, sum, quantity, vat, vat_sum, price, category_id):
        ''' Удаление товара из базы данных '''
        await self.connection()
        # Получение product_name_id
        await self.cursor.execute(f"SELECT id FROM product_names WHERE name = '{product_name}'")
        product_name_id = await self.cursor.fetchone()

        # Получение product_name_id
        await self.cursor.execute(f"SELECT id FROM receipts WHERE receipt = '{receipt}'")
        receipt_id = await self.cursor.fetchone()

        # Удаление товара из БД
        await self.cursor.execute(f"DELETE FROM products WHERE product_name_id = {product_name_id[0]} and sum = {sum} and quantity = {quantity} and vat = {vat} and vat_sum = {vat_sum} and price = {price} and receipt_id = {receipt_id[0]} and category_id = {category_id}")
        await self.db.commit()

        await self.cursor.close()
        self.db.close()

        return True

    @classmethod
    async def get_categories(self):
        ''' Получение списка категорий из базы данных '''
        await self.connection()
        # Получение списка категорий нижнего уровня
        await self.cursor.execute('select id, name, tags from categories where tags is not null')
        categories = await self.cursor.fetchall()
        
        await self.cursor.close()
        self.db.close()

        return categories

    # def create_db():
    #     # Создание таблицы пользователей, если её нет
    #     cursor.execute('CREATE TABLE IF NOT EXISTS users(' +
    #         'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
    #         'telegram_id INTEGER NOT NULL,' +
    #         'role INTEGER DEFAULT 0' +
    #         ')')
    #     db.commit()

    #     # Создание таблицы магазинов, если её нет
    #     cursor.execute('CREATE TABLE IF NOT EXISTS stores(' +
    #         'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
    #         'name VARCHAR(255),' +
    #         'address VARCHAR(255)' +
    #         ')')
    #     db.commit()

    #     # Создание таблицы чеков, если её нет
    #     cursor.execute('CREATE TABLE IF NOT EXISTS receipts(' +
    #         'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
    #         'receipt TEXT NOT NULL,' +
    #         'date VARCHAR(255) NOT NULL,' +
    #         'user_id INTEGER NOT NULL,' +
    #         'store_id INTEGER NOT NULL,' +
    #         'FOREIGN KEY (user_id) REFERENCES users (id),' +
    #         'FOREIGN KEY (store_id) REFERENCES stores (id)' +
    #         ')')
    #     db.commit()

    #     # Создание таблицы наименования товаров, если её нет
    #     cursor.execute('CREATE TABLE IF NOT EXISTS product_names(' +
    #         'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
    #         'name VARCHAR(255)' +
    #         ')')
    #     db.commit()

    #     # Создание таблицы категорий, если её нет
    #     cursor.execute('CREATE TABLE IF NOT EXISTS categories(' +
    #         'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
    #         'name VARCHAR(255),' +
    #         'tags TEXT,' +
    #         'category_id INTEGER DEFAULT NULL,' +
    #         'FOREIGN KEY (category_id) REFERENCES categories (id),' +
    #         'UNIQUE (name)' +
    #         ')')
    #     db.commit()

    #     # Создание таблицы товаров, если её нет
    #     cursor.execute('CREATE TABLE IF NOT EXISTS products(' +
    #         'id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,' +
    #         'product_name_id INTEGER NOT NULL,' +
    #         'sum FLOAT,' +
    #         'quantity FLOAT,' +
    #         'vat TINYINT,' +
    #         'vat_sum FLOAT,' +
    #         'price FLOAT,' +
    #         'receipt_id INTEGER NOT NULL,' +
    #         'category_id INTEGER NOT NULL,' +
    #         'FOREIGN KEY (receipt_id) REFERENCES receipts (id),' +
    #         'FOREIGN KEY (category_id) REFERENCES categories (id),' +
    #         'FOREIGN KEY (product_name_id) REFERENCES product_names (id)' +
    #         ')')
    #     db.commit()
