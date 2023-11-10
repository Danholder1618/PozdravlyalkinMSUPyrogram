import os
import config
import text
import db_functions
import requests
import asyncio

from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Функция для удаления сообщения по его идентификатору после определенного времени
async def delete_message(chat_id, message_id, delay_seconds, app):
    await asyncio.sleep(delay_seconds)
    await app.delete_messages(chat_id, message_id)

async def make_image():
    response = requests.get(config.PIC_PLACE)
    im = Image.open(BytesIO(response.content))

    # Вотермарка
    response = requests.get(config.LOGO_PLACE)
    watermark = Image.open(BytesIO(response.content)).convert("RGBA")
    mask = Image.new("L", watermark.size, 128)
    im.paste(watermark, (25, 25), mask)

    # Текст
    font1 = ImageFont.truetype("arial.ttf", size=50)
    font2 = ImageFont.truetype("arial.ttf", size=20)
    draw_text = ImageDraw.Draw(im)
    draw_text.text((100, 250), 'С Днём Рождения!', font=font1, fill='#ffd700')

    current_date = datetime.now().strftime("%d.%m")
    current_date = "'" + current_date + "'"

    bd_tuday = db_functions.name_and_group_get(current_date)
    x = 200
    y = 300

    q = len(bd_tuday)
    for i in range(q):
        if (bd_tuday[i][3] == 1):
            y = y + 50
            draw_text.text((x, y), f'{(bd_tuday[i][0])[:-1]}, группа: {bd_tuday[i][2]} !', font=font2, fill='#ffffff')

    draw_text.text((100, y+100), 'Вот так вот', font=font1, fill='#ffd700')

    #im.show()

    image_stream = BytesIO()
    # Сохраняем изображение в байтовый поток в формате PNG
    im.save(image_stream, format="PNG")
    image_stream.seek(0)
    return(im)