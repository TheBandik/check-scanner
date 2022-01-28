import os

import pyzbar.pyzbar as pz
import PIL

import db


def scan(user_id, image):
    receipt = pz.decode(PIL.Image.open(image))
    print(receipt[0][0])
    os.remove(image)
    # db.add_receipt(user_id, receipt)
