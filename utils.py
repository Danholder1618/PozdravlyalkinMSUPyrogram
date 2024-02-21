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

#def get_contrast_color(background_color):
#    brightness = sum(background_color) / 3
#    return 1 if brightness < 128 else 2
#
#def get_contrast_logo(color_index):
#    return config.LOGO_YELLOW if color_index == 1 else config.LOGO_RED

async def delete_message(chat_id, group_id, app):
    try:
        with open('message_ids.txt', 'r') as file:
            saved_message_ids = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        saved_message_ids = []

    messages_to_delete = saved_message_ids[-4:]
    for msg_id in messages_to_delete:
        try:
            await app.delete_messages(group_id, msg_id)
        except Exception as e:
            logging.error(f"Error deleting message {msg_id}: {e}")

    # await app.send_message(chat_id, "Картинка удалена")

async def make_image(people_to_congratulate):
    pic_path = await random_pic()
    pic_index = config.PIC_PLACE.index(pic_path)

    # Выбор цвета текста и логотипа в зависимости от выбранной картинки
    if pic_index < 12:
        text_color = "#E8CB52"
        logo_path = config.LOGO_YELLOW
    else:
        text_color = "#A60B38"
        logo_path = config.LOGO_RED

    im = Image.open(pic_path)

    # Вотермарка
    watermark = Image.open(logo_path).convert("RGBA")
    watermark = watermark.resize((300, 300))
    im.paste(watermark, (25, 25), watermark)

    # Текст
    font1 = ImageFont.truetype("georgia.ttf", size=80)
    font2 = ImageFont.truetype("cour.ttf", size=60)
    font3 = ImageFont.truetype("georgia.ttf", size=65)
    bold_font2 = ImageFont.truetype("courbd.ttf", size=60)
    draw_text = ImageDraw.Draw(im)

    # Добавление черного обрамления с небольшой прозрачностью для красивого эффекта
    x = 360
    y = 120
    for i in range(-2, 3):
        for j in range(-2, 3):
            draw_text.text((x + i, y + j), text.pordr_verh, font=font1, fill="#000000", alpha=150)

    draw_text.text((x, y), text.pordr_verh, font=font1, fill=text_color)

    q = len(people_to_congratulate)
    if q == 1:
        if people_to_congratulate[0][3] == 1:
            case = 1
        else:
            case = 3
    else:
        ch = sum(1 for entry in people_to_congratulate if entry[3] == 1)
        if ch == q:
            case = 2
        elif ch == 0:
            case = 4
        else:
            case = 5

    pozdr_niz = await random_congratulation(case)

    x = 110
    y = 270
    for entry in people_to_congratulate:
        y += 50
        max_line_length = 25
        name_parts = entry[0].strip().split()[:2]
        fi = ' '.join(name_parts)
        if entry[3] == 1:
            text_to_wrap = f'{fi.strip()}, {entry[2].strip()}'
        else:
            text_to_wrap = f'! {fi.strip()} !'

        wrapped_text = textwrap.wrap(text_to_wrap, width=max_line_length)
        first_line_indent = 30
        new_x = x
        for line in wrapped_text:
            for i in range(-2, 3):
                for j in range(-2, 3):
                    draw_text.text((new_x + i, y + j), line, font=font2, fill="#000000", alpha=150)
            draw_text.text((new_x, y), line, font=bold_font2 if entry[3] == 1 else font2, fill=text_color)
            y += 50
            new_x += first_line_indent
            first_line_indent = 0

    y += 30
    max_line_length = 27
    wrapped_text = textwrap.wrap(pozdr_niz, width=max_line_length)

    first_line_indent = 30
    new_x = 70
    y = 750
    for line in wrapped_text:
        for i in range(-2, 3):
            for j in range(-2, 3):
                draw_text.text((new_x + i, y + j), line, font=font3, fill="#000000", alpha=150)
        draw_text.text((new_x, y), line, font=font3, fill=text_color)
        y += 50
        new_x -= first_line_indent
        first_line_indent = 0

    im.save('temp.png', format="PNG")
