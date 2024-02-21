import asyncio
import config
import db_functions
import utils
from datetime import datetime
from pyrogram import Client
from my_bot import birthday

api_id = config.APP_API_ID
api_hash = config.APP_API_HASH
bot_token = config.BOT_TEST_TOKEN
group_id = config.TEST_CHANEL
chat_id = config.MY_ID

async def send_congratulation(app):
    now = datetime.now()
    current_date = now.strftime("%d.%m")
    bd_today = db_functions.name_and_group_get(current_date)
    last_congratulation_sent = await utils.get_congratulation_status()

    # await app.send_message(chat_id, f"Статус {'Отправлено' if last_congratulation_sent == 1 else 'Не Отправлено'}")

    if bd_today and not last_congratulation_sent:
        # await app.send_message(chat_id, "Сегодня кто-то родился, поздравление отправляется")
        num_images = -(-len(bd_today) // 3)
        for i in range(num_images):
            start_idx = i * 3
            end_idx = min((i + 1) * 3, len(bd_today))
            people_to_congratulate = bd_today[start_idx:end_idx]

            await birthday(app, group_id, chat_id, people_to_congratulate)
            await utils.save_congratulation_status(1)
    # else:
        # await app.send_message(chat_id, "Сегодня никто не родился (либо это перезапуск), поздравление не отправляется")

async def scheduler_task():
    app = Client("Поздравлялкин", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    await app.start()
    await app.send_message(chat_id, "Бот начал работу")

    while True:
        now = datetime.now()
        if now.hour >= 8 and now.minute >= 0:
            last_congratulation_sent = await utils.get_congratulation_status()
            if not last_congratulation_sent:
                await utils.delete_message(chat_id, group_id, app)
                await send_congratulation(app)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(scheduler_task())
