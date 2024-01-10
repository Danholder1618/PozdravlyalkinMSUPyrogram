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
    return random.choice(text.pozdr_list).rstrip()

async def random_pic():
    return random.choice(config.PIC_PLACE).rstrip()

async def delete_message(chat_id, message_id, delay_seconds, app):
    await asyncio.sleep(delay_seconds)
    await app.delete_messages(chat_id, message_id)

def get_contrast_color(background_color):
    brightness = sum(background_color) / 3
    return "#E8CB52" if brightness < 128 else "#A60B38"

async def make_image():
    im = Image.open(await random_pic()) 
    pozdr_niz = await random_congratulation()

    # Цвет текста на основе контраста
    background_color = im.getpixel((100, 250))
    text_color = get_contrast_color(background_color)

    # Вотермарка
    watermark_color = "#E8CB52"  
    if text_color == "#A60B38":
        watermark_color = "#A60B38" 

    watermark = Image.open(BytesIO(config.LOGO_WHITE))  
    watermark = watermark.convert("RGBA")
    watermark = watermark.resize((250, 250))
    watermark.putalpha(128)  

    if text_color == "#A60B38":
        watermark = Image.open(BytesIO(config.LOGO_BLACK))  
        watermark = watermark.convert("RGBA")
        watermark = watermark.resize((250, 250))
        watermark.putalpha(128)  

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
