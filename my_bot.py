import asyncio
import datetime
import config
import utils
import sqlite3

from pyrogram import Client

# Отправка фотографии каждый день в 8 часов
async def birthday(app):
    chat_id = config.CHAT_ID
    img = await utils.make_image()
    img.save('temp.png')
    photo_path = config.BG_PATH

    # Получение информации о текущем пользователе (боте)
    me = await app.get_me()

    # Какой-то там премиум
    if me is not None and hasattr(me, 'is_premium'):
        file_size_limit_mib = 4000 if me.is_premium else 2000
    else:
        file_size_limit_mib = 2000

    msg = await app.send_photo(chat_id, photo_path, "Тута тоже текст можно")
    await utils.delete_message(chat_id, msg, 86360, app)