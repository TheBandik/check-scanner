''' Модуль для тестирования модуля db '''

import os
import sys

import pytest

sys.path.append(os.path.abspath('../src'))
import db


@pytest.mark.asyncio
async def test_connection():
    assert await db.DataBase.connection() == True
    await db.DataBase.cursor.close()
    db.DataBase.db.close()

@pytest.mark.asyncio
async def test_add_user():
    assert await db.DataBase.add_user(512570420) == True

@pytest.mark.asyncio
async def test_add_store():
    assert await db.DataBase.add_store('Реми 24', '690039, Приморский край, г.Владивосток, ул.Русская 5 к') == True

@pytest.mark.asyncio
async def test_add_receipt():
    assert await db.DataBase.add_receipt(512570420, 't=20220318T145452&s=189.90&fn=9960440300879933&i=61704&fp=3919420163&n=1', 'Реми 24', '2021-12-29T11:34:00') == True

@pytest.mark.asyncio
async def test_add_product_name():
    assert await db.DataBase.add_product_name('МАНДАРИНЫ ЮАР 1КГ')

@pytest.mark.asyncio
async def test_add_product():
    assert await db.DataBase.add_product('МАНДАРИНЫ ЮАР 1КГ', 't=20220318T145452&s=189.90&fn=9960440300879933&i=61704&fp=3919420163&n=1', 120, 1, 1, 10, 120, 12)

@pytest.mark.asyncio
async def test_delete_product():
    assert await db.DataBase.delete_product('МАНДАРИНЫ ЮАР 1КГ', 't=20220318T145452&s=189.90&fn=9960440300879933&i=61704&fp=3919420163&n=1', 120, 1, 1, 10, 120, 12)

@pytest.mark.asyncio
async def test_delete_product_name():
    assert await db.DataBase.delete_product_name('МАНДАРИНЫ ЮАР 1КГ')

@pytest.mark.asyncio
async def test_delete_receipt():
    assert await db.DataBase.delete_receipt('t=20220318T145452&s=189.90&fn=9960440300879933&i=61704&fp=3919420163&n=1') == True

@pytest.mark.asyncio
async def test_delete_store():
    assert await db.DataBase.delete_store('Реми 24', '690039, Приморский край, г.Владивосток, ул.Русская 5 к') == True

@pytest.mark.asyncio
async def test_delete_user():
    assert await db.DataBase.delete_user(512570420) == True
