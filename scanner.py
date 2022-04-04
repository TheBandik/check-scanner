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
            for item in receipt['data']['json']['items']:
                products.append(f"{item['name']}: {int(item['sum']) / 100}")
            return products
        except:
            return '0'
    else:
        return '1'
