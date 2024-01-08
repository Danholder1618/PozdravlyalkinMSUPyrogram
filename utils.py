import os
import config
import db_functions
import random
import asyncio
import text

from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

async def random_congratulation():
    return random.choice(text.pozdr_list).strip()

# Функция для удаления сообщения по его идентификатору после определенного времени
async def delete_message(chat_id, message_id, delay_seconds, app):
    await asyncio.sleep(delay_seconds)
    await app.delete_messages(chat_id, message_id)

def get_contrast_color(background_color):
    # Простой алгоритм для определения контрастного цвета (темно-желтый или темно-синий)
    brightness = sum(background_color) / 3
    return "#E8CB52" if brightness < 128 else "#A60B38"

async def make_image():
    im = Image.open(config.PIC_PLACE) 
    pozdr_niz = await random_congratulation()

    # Вотермарка
    watermark = Image.open(config.LOGO_PLACE).convert("RGBA")
    mask = Image.new("L", watermark.size, 128)
    im.paste(watermark, (25, 25), mask)

    # Текст
    font1 = ImageFont.truetype("arial.ttf", size=70)
    font2 = ImageFont.truetype("arial.ttf", size=40)
    font3 = ImageFont.truetype("arial.ttf", size=40)
    draw_text = ImageDraw.Draw(im)
    
    # Цвет текста на основе контраста
    background_color = im.getpixel((100, 250))  # Пример координат для определения цвета фона
    text_color = get_contrast_color(background_color)

    # Добавление черного обрамления для лучшей видимости текста
    draw_text.text((300-1, 100-1), f'{text.pordr_verh}', font=font1, fill="#000000")  
    draw_text.text((300+1, 100-1), f'{text.pordr_verh}', font=font1, fill="#000000")
    draw_text.text((300-1, 100+1), f'{text.pordr_verh}', font=font1, fill="#000000")
    draw_text.text((300+1, 100+1), f'{text.pordr_verh}', font=font1, fill="#000000")
    draw_text.text((300, 100), f'{text.pordr_verh}', font=font1, fill=text_color)

    current_date = datetime.now().strftime("%d.%m")
    current_date = "'" + current_date + "'"

    bd_tuday = db_functions.name_and_group_get(current_date)
    x = 300
    y = 200

    q = len(bd_tuday)
    for i in range(q):
        if bd_tuday[i][3] == 1:
            y = y + 50
        # Определение максимальной высоты для текста (высота изображения минус отступ)
        max_text_height = im.size[1] - 50

        q = len(bd_tuday)
        for i in range(q):
            if bd_tuday[i][3] == 1:
                y = y + 50
                # Проверка на выход за пределы изображения
                if y + 50 > max_text_height:
                    y = 200  # Возвращение на начальную позицию
                # Аналогично для второго шрифта
                draw_text.text((x-1, y-1), f'{bd_tuday[i][0][:-1]}, группа: {bd_tuday[i][2]} !', font=font2, fill="#000000")
                draw_text.text((x+1, y-1), f'{bd_tuday[i][0][:-1]}, группа: {bd_tuday[i][2]} !', font=font2, fill="#000000")
                draw_text.text((x-1, y+1), f'{bd_tuday[i][0][:-1]}, группа: {bd_tuday[i][2]} !', font=font2, fill="#000000")
                draw_text.text((x+1, y+1), f'{bd_tuday[i][0][:-1]}, группа: {bd_tuday[i][2]} !', font=font2, fill="#000000")
                draw_text.text((x, y), f'{bd_tuday[i][0][:-1]}, группа: {bd_tuday[i][2]} !', font=font2, fill=text_color)


    draw_text.text((100-1, y+100-1), f'{pozdr_niz}', font=font3, fill="#000000")  
    draw_text.text((100+1, y+100-1), f'{pozdr_niz}', font=font3, fill="#000000")
    draw_text.text((100-1, y+100+1), f'{pozdr_niz}', font=font3, fill="#000000")
    draw_text.text((100+1, y+100+1), f'{pozdr_niz}', font=font3, fill="#000000")
    draw_text.text((100, y+100), f'{pozdr_niz}', font=font3, fill=text_color)

    im.save('temp.png', format="PNG")
