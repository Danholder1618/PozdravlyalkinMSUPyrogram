import config
import db_functions
import random
import asyncio
import text
import textwrap

from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

async def random_congratulation():
    return random.choice(text.pozdr_list).strip()

async def random_pic():
    return random.choice(config.PIC_PLACE).strip()

# Функция для удаления сообщения по его идентификатору после определенного времени
async def delete_message(chat_id, message_id, delay_seconds, app):
    await asyncio.sleep(delay_seconds)
    await app.delete_messages(chat_id, message_id)

def get_contrast_color(background_color):
    # Простой алгоритм для определения контрастного цвета (темно-желтый или темно-синий)
    brightness = sum(background_color) / 3
    return "#E8CB52" if brightness < 128 else "#A60B38"

async def make_image():
    im = Image.open(await random_pic()) 
    pozdr_niz = await random_congratulation()

    # Вотермарка
    watermark = Image.open(config.LOGO_PLACE).convert("RGBA")
    mask = Image.new("L", watermark.size, 128)
    im.paste(watermark, (25, 25), mask)

    # Текст
    font1 = ImageFont.truetype("georgia.ttf", size=70)
    font2 = ImageFont.truetype("cour.ttf", size=45)
    font3 = ImageFont.truetype("georgia.ttf", size=50)
    draw_text = ImageDraw.Draw(im)
    
    # Цвет текста на основе контраста
    background_color = im.getpixel((100, 250))  # Пример координат для определения цвета фона
    text_color = get_contrast_color(background_color)

    # Добавление черного обрамления для лучшей видимости текста
    draw_text.text((320-1, 100-1), f'{text.pordr_verh}', font=font1, fill="#000000")  
    draw_text.text((320+1, 100-1), f'{text.pordr_verh}', font=font1, fill="#000000")
    draw_text.text((320-1, 100+1), f'{text.pordr_verh}', font=font1, fill="#000000")
    draw_text.text((320+1, 100+1), f'{text.pordr_verh}', font=font1, fill="#000000")
    draw_text.text((320, 100), f'{text.pordr_verh}', font=font1, fill=text_color)

    current_date = datetime.now().strftime("%d.%m")
    current_date = "'" + current_date + "'"

    bd_tuday = db_functions.name_and_group_get(current_date)
    x = 280
    y = 160

    q = len(bd_tuday)
    for i in range(q):
        y = y + 50
        if bd_tuday[i][3] == 1:

            max_line_length = 35

            text_to_wrap = f'{bd_tuday[i][0]}, группа: {bd_tuday[i][2]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x-1, new_y-1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'{bd_tuday[i][0]}, группа: {bd_tuday[i][2]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x+1, new_y-1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'{bd_tuday[i][0]}, группа: {bd_tuday[i][2]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x-1, new_y+1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'{bd_tuday[i][0]}, группа: {bd_tuday[i][2]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x+1, new_y+1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'{bd_tuday[i][0]}, группа: {bd_tuday[i][2]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x, new_y), line, font=font2, fill=text_color)
                new_y += 50
                new_x = x-20

        else:
            max_line_length = 35

            text_to_wrap = f'! {bd_tuday[i][0]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x-1, new_y-1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'! {bd_tuday[i][0]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x+1, new_y-1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'! {bd_tuday[i][0]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x-1, new_y+1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'! {bd_tuday[i][0]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x+1, new_y+1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'! {bd_tuday[i][0]} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x, new_y), line, font=font2, fill=text_color)
                new_y += 50
                new_x = x-20

    y += 20
    max_line_length = 35
    text_to_wrap = f'{pozdr_niz}'
    wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)

    new_y = y + 50
    new_x = 100
    for line in wrapped_text:
        draw_text.text((new_x-1, new_y-1), line, font=font3, fill="#000000")
        new_y += 50
        new_x = 100-30
    new_y = y + 50
    new_x = 100
    for line in wrapped_text: 
        draw_text.text((new_x+1, new_y-1), line, font=font3, fill="#000000")
        new_y += 50
        new_x = 100-30
    new_y = y + 50
    new_x = 100
    for line in wrapped_text:
        draw_text.text((new_x-1, new_y+1), line, font=font3, fill="#000000")
        new_y += 50
        new_x = 100-30
    new_y = y + 50
    new_x = 100
    for line in wrapped_text:
        draw_text.text((new_x+1, new_y+1), line, font=font3, fill="#000000")
        new_y += 50
        new_x = 100-30
    new_y = y + 50
    new_x = 100
    for line in wrapped_text:
        draw_text.text((new_x, new_y), line, font=font3, fill=text_color)
        new_y += 50
        new_x = 100-30

    im.save('temp.png', format="PNG")
