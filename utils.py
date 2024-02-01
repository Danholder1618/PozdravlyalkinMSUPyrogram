import config
import db_functions
import random
import asyncio
import text
import textwrap
import os

from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

async def save_congratulation_status(sent):
    with open('congratulation_status.txt', 'w') as file:
        file.write(str(sent))

async def get_congratulation_status():
    try:
        with open('congratulation_status.txt', 'r') as file:
            content = file.read().strip()
            return int(content) if content else 0
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


async def save_message_id(message_id):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'message_ids.txt')

    with open(file_path, 'a') as file:
        file.write(f"{message_id}\n")

async def random_congratulation():
    return random.choice(text.pozdr_list).rstrip()

async def random_pic():
    return random.choice(config.PIC_PLACE).rstrip()

async def delete_message(chat_id, delay_seconds, app):
    await asyncio.sleep(delay_seconds)

    # Загрузка сохраненных айди сообщений
    try:
        with open('message_ids.txt', 'r') as file:
            saved_message_ids = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        saved_message_ids = []

    # Безопасное удаление последних сообщений (максимум двух)
    messages_to_delete = saved_message_ids[-2:]
    for msg_id in messages_to_delete:
        try:
            await app.delete_messages(chat_id, msg_id)
        except Exception as e:
            print(f"Error deleting message {msg_id}: {e}")

def get_contrast_color(background_color):
    brightness = sum(background_color) / 3
    return 1 if brightness < 128 else 2

def get_contrast_logo(color_index):
    return config.LOGO_WHITE if color_index == 1 else config.LOGO_BLACK

async def make_image():
    im = Image.open(await random_pic()) 
    pozdr_niz = await random_congratulation()

    # Цвет текста на основе контраста
    background_color = im.getpixel((100, 250))
    color_index = get_contrast_color(background_color)
    if (color_index == 1): text_color = "#E8CB52"
    else: text_color = "#A60B38"

    # Вотермарка
    watermark = Image.open(get_contrast_logo(color_index)).convert("RGBA")
    watermark = watermark.resize((250, 250))
    im.paste(watermark, (25, 25), watermark)

    # Текст
    font1 = ImageFont.truetype("georgia.ttf", size=70)
    font2 = ImageFont.truetype("cour.ttf", size=48)
    font3 = ImageFont.truetype("georgia.ttf", size=50)
    draw_text = ImageDraw.Draw(im)

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
        max_line_length = 30
        if bd_tuday[i][3] == 1:

            name_parts = bd_tuday[i][0].strip().split()[:2]
            fi = ' '.join(name_parts)

            text_to_wrap = f'{fi.strip()}, {bd_tuday[i][2].strip()}'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x-1, new_y-1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'{fi.strip()}, {bd_tuday[i][2].strip()}'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x+1, new_y-1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'{fi.strip()}, {bd_tuday[i][2].strip()}'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x-1, new_y+1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'{fi.strip()}, {bd_tuday[i][2].strip()}'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x+1, new_y+1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'{fi.strip()}, {bd_tuday[i][2].strip()}'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x, new_y), line, font=font2, fill=text_color)
                new_y += 50
                new_x = x-20
            y += 30

        else:

            name_parts = bd_tuday[i][0].strip().split()[:2]
            fi = ' '.join(name_parts)

            text_to_wrap = f'! {fi.strip()} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x-1, new_y-1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'! {fi.strip()} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x+1, new_y-1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'! {fi.strip()} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x-1, new_y+1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'! {fi.strip()} !'
            wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
            new_y = y
            new_x = x
            for line in wrapped_text:
                draw_text.text((new_x+1, new_y+1), line, font=font2, fill="#000000")
                new_y += 50
                new_x = x-20
            text_to_wrap = f'! {fi.strip()} !'
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
