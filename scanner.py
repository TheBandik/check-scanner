import os

import pyzbar.pyzbar as pz
import PIL
import requests

import db
import parser


def scan(user_id, image):
    receipt = pz.decode(PIL.Image.open(image))
    os.remove(image)
    if receipt:
        db.add_receipt(user_id, receipt[0][0].decode("utf-8"))
        data = parser.create_data(receipt[0][0].decode("utf-8"))
        receipt = requests.post(f'https://proverkacheka.com/api/v1/check/get', data=data).json()
        products = []
        try:
            products.append(f"{receipt['data']['json']['retailPlace']}")
            for item in receipt['data']['json']['items']:
                products.append(f"{item['name']}\n<b>{int(item['sum']) / 100} ₽ / НДС: {int(item['ndsSum']) / 100} ₽</b>")
            divider = '_' * len(f"Итого: {int(receipt['data']['json']['totalSum']) / 100} ₽ ")
            products.append(f"{divider}\n<b>Итого: {int(receipt['data']['json']['totalSum']) / 100} ₽\nНДС: {int(receipt['data']['json']['nds10']) / 100} ₽ (10%) / {int(receipt['data']['json']['nds18']) / 100} ₽ (20%)\nИтого НДС: {int(receipt['data']['json']['nds10']) / 100 + int(receipt['data']['json']['nds18']) / 100} ₽</b>")

            return products
        except:
            return '0'
    else:
        return '1'
