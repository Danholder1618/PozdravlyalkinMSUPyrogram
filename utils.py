import config
import db_functions
import random
import asyncio
import aiofiles
import logging
import text
import textwrap
import os

from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

async def save_congratulation_status(sent):
    date = datetime.now().strftime("%d.%m")
    with open('congratulation_status.txt', 'w') as file:
        file.write(f"{date},{sent}")

async def get_congratulation_status():
    try:
        with open('congratulation_status.txt', 'r') as file:
            content = file.read().strip()
            if content:
                date, status = content.split(',')
                if date == datetime.now().strftime("%d.%m"):
                    return int(status)
                else:
                    return 0
            else:
                return 0
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0

async def save_message_id(message_id):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'message_ids.txt')

    async with aiofiles.open(file_path, 'a+') as file:
        await file.write(f"{message_id}\n")

async def random_congratulation(case):
    if case == 1:
        return random.choice(text.pozdr_list_one_student).rstrip()
    if case == 2:
        return random.choice(text.pozdr_list_multiple_student).rstrip()
    if case == 3:
        return random.choice(text.pozdr_list_one_teacher).rstrip()
    if case == 4:
        return random.choice(text.pozdr_list_multiple_teacher).rstrip()
    if case == 5:
        return random.choice(text.pozdr_list_both).rstrip()

async def random_pic():
    try:
        pic_path = random.choice(config.PIC_PLACE).rstrip()
        if os.path.exists(pic_path):
            return pic_path
        else:
            raise FileNotFoundError("File not found")
    except Exception as e:
        logging.error(f"Error selecting random picture: {e}")
        return None

async def delete_message(chat_id, group_id, app):
    try:
        with open('message_ids.txt', 'r') as file:
            saved_message_ids = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        saved_message_ids = []

    messages_to_delete = saved_message_ids[-2:]
    for msg_id in messages_to_delete:
        try:
            await app.delete_messages(group_id, msg_id)
        except Exception as e:
            logging.error(f"Error deleting message {msg_id}: {e}")

    await app.send_message(chat_id, "Картинка удалена")

async def make_image():
    im = Image.open(await random_pic())

    # Выбор цвета текста и логотипа в зависимости от выбранной картинки
    if 1 <= random.randint(1, 12) <= 6:
        text_color = "#E8CB52"
        logo_path = config.LOGO_WHITE
    else:
        text_color = "#A60B38"
        logo_path = config.LOGO_BLACK

    # Вотермарка
    watermark = Image.open(logo_path).convert("RGBA")
    watermark = watermark.resize((300, 300))
    im.paste(watermark, (25, 25), watermark)

    # Текст
    font1 = ImageFont.truetype("georgia.ttf", size=80)
    font2 = ImageFont.truetype("cour.ttf", size=60)
    font3 = ImageFont.truetype("georgia.ttf", size=65)
    draw_text = ImageDraw.Draw(im)

    # Добавление черного обрамления для лучшей видимости текста
    x = 360
    y = 120
    for i in range(-1, 2):
        for j in range(-1, 2):
            draw_text.text((x + i, y + j), text.pordr_verh, font=font1, fill="#000000")

    draw_text.text((x, y), text.pordr_verh, font=font1, fill=text_color)

    current_date = datetime.now().strftime("%d.%m")
    current_date = "'" + current_date + "'"

    bd_today = db_functions.name_and_group_get(current_date)

    q = len(bd_today)
    if q == 1:
        if bd_today[0][3] == 1:
            case = 1
        else:
            case = 3
    else:
        ch = sum(1 for entry in bd_today if entry[3] == 1)
        if ch == q:
            case = 2
        elif ch == 0:
            case = 4
        else:
            case = 5

    pozdr_niz = await random_congratulation(case)

    x = 150
    y = 265
    for entry in bd_today:
        y += 50
        max_line_length = 25
        name_parts = entry[0].strip().split()[:2]
        fi = ' '.join(name_parts)
        if entry[3] == 1:
            text_to_wrap = f'{fi.strip()}, {entry[2].strip()}'
        else:
            text_to_wrap = f'! {fi.strip()} !'

        wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
        new_x = x - 20
        for line in wrapped_text:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    draw_text.text((new_x + i, y + j), line, font=font2, fill="#000000")
            draw_text.text((new_x, y), line, font=font2, fill=text_color)
            y += 50

    y += 20
    max_line_length = 30
    wrapped_text = textwrap.wrap(pozdr_niz, width=max_line_length)

    new_x = 100 - 30
    for line in wrapped_text:
        for i in range(-1, 2):
            for j in range(-1, 2):
                draw_text.text((new_x + i, y + j), line, font=font3, fill="#000000")
        draw_text.text((new_x, y), line, font=font3, fill=text_color)
        y += 50

    im.save('temp.png', format="PNG")
