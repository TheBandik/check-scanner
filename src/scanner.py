import os

import pyzbar.pyzbar as pz
import PIL
import requests

import db
import parser


# Сканирование QR-кода
def scan(user_id, image):
    # Распознование QR-кода
    receipt = pz.decode(PIL.Image.open(image))
    # Удаление локального изображения
    os.remove(image)
    if receipt:
        # Добавление чека в БД
        db.add_receipt(user_id, receipt[0][0].decode("utf-8"))
        # Получение словаря данных из QR-кода для отправки по api
        data = parser.create_data(receipt[0][0].decode("utf-8"))
        # Получение чека из ФНС
        receipt = requests.post(f'https://proverkacheka.com/api/v1/check/get', data=data).json()
        products = []
        try:
            # Формирование списка товаров для отправки пользователю
            # products.append(f"{receipt['data']['json']['retailPlace']}")
            for item in receipt['data']['json']['items']:
                products.append(f"{item['name']}\n<b>{int(item['sum']) / 100} ₽ / НДС: {int(item['ndsSum']) / 100} ₽</b>")
            # divider = '_' * len(f"Итого: {int(receipt['data']['json']['totalSum']) / 100} ₽ ")
            # products.append(f"{divider}\n<b>Итого: {int(receipt['data']['json']['totalSum']) / 100} ₽\nНДС: {int(receipt['data']['json']['nds10']) / 100} ₽ (10%) / {int(receipt['data']['json']['nds18']) / 100} ₽ (20%)\nИтого НДС: {int(receipt['data']['json']['nds10']) / 100 + int(receipt['data']['json']['nds18']) / 100} ₽</b>")

            return products
        except:
            return '0'
    else:
        return '1'
