import sqlite3


connect = sqlite3.connect('products.db', check_same_thread=False)
cursor = connect.cursor()

def add_user(user_id):
    cursor.execute('CREATE TABLE IF NOT EXISTS users(' +
        'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,' +
        'tel_id INTEGER NOT NULL' +
        ')')
    connect.commit()

    cursor.execute(f'SELECT tel_id FROM users WHERE tel_id = {user_id}')
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f'INSERT INTO users(tel_id) VALUES({user_id})')
        connect.commit()

def add_receipt(user_id, receipt):
    cursor.execute('CREATE TABLE IF NOT EXISTS receipts(' +
        'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,' +
        'receipt TEXT NOT NULL,' +
        'user_id INTEGER NOT NULL,' +
        'FOREIGN KEY (user_id) REFERENCES users(id)' +
        ')')
    connect.commit()
    cursor.execute(f"SELECT receipt FROM receipts WHERE receipt = '{receipt}'")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO receipts(receipt, user_id) VALUES('{receipt}', {user_id})")
        connect.commit()
