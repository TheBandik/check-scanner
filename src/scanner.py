import os
import re
import asyncio

import pyzbar.pyzbar as pz
import PIL
import requests

import db
import settings
import categorization


# Создание словаря данных для отправки по api
def create_data(receipt):
    # Получение нужно части информации из QR-кода
    receipt = re.sub('[tsfnip=]', '', receipt)
    receipt = receipt.split('&')

    # Формирование словаря
    data = {
        'fn': receipt[2],
        'fd': receipt[3],
        'fp': receipt[4],
        't': receipt[0],
        'n': receipt[5],
        's': receipt[1],
        'qr': '1',
        'token': settings.api_token
    }
    
    return data

# Сканирование QR-кода
def scan(user_id, image, bot):
    # Распознование QR-кода
    qr = pz.decode(PIL.Image.open(image))
    # Удаление локального изображения
    os.remove(image)
    if qr:
        # Получение словаря данных из QR-кода для отправки по api
        data = create_data(qr[0][0].decode("utf-8"))
        # Получение чека из ФНС
        receipt = requests.post(f'https://proverkacheka.com/api/v1/check/get', data=data).json()
        if len(receipt.keys()) > 2:
            bot.send_message(user_id, 'Чек получен, ожидайте распределение товаров по категориям...')
            products = []
            # Добавление магазина в БД
            asyncio.run(db.DataBase.add_store(receipt['data']['json']['retailPlace'], receipt['data']['json']['retailPlaceAddress']))
            # Добавление чека в БД
            asyncio.run(db.DataBase.add_receipt(user_id, qr[0][0].decode("utf-8"), receipt['data']['json']['retailPlace'], receipt['data']['json']['dateTime']))


            for item in receipt['data']['json']['items']:
                # Добавление имени товара
                asyncio.run(db.DataBase.add_product_name(item['name']))

                # Определение категории товара
                category = categorization.category_detection(item['name'])
                # Добавление товара
                asyncio.run(db.DataBase.add_product(item['name'], qr[0][0].decode("utf-8"), int(item['sum']) / 100, item['quantity'], item['nds'], int(item['ndsSum']) / 100, int(item['price']) / 100, category))
        

            # Формирование списка товаров для отправки пользователю
            # products.append(f"{receipt['data']['json']['retailPlace']}")
            for item in receipt['data']['json']['items']:
                products.append(f"{item['name']}\n<b>{int(item['sum']) / 100} ₽ / НДС: {int(item['ndsSum']) / 100} ₽</b>")
            # divider = '_' * len(f"Итого: {int(receipt['data']['json']['totalSum']) / 100} ₽ ")
            # products.append(f"{divider}\n<b>Итого: {int(receipt['data']['json']['totalSum']) / 100} ₽\nНДС: {int(receipt['data']['json']['nds10']) / 100} ₽ (10%) / {int(receipt['data']['json']['nds18']) / 100} ₽ (20%)\nИтого НДС: {int(receipt['data']['json']['nds10']) / 100 + int(receipt['data']['json']['nds18']) / 100} ₽</b>")

            return products
        else:
            return '0'
    else:
        return '1'
