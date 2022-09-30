import re

import settings


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
