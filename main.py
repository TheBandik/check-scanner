import json

import requests

import settings


bill = requests.post(f'https://proverkacheka.com/api/v1/check/get', data=settings.data).json()
print(bill['data']['json']['items'])

with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(bill, ensure_ascii=False))
