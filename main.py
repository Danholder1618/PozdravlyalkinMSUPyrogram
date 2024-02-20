import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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

app = Client("Поздравлялкин", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

async def send_congratulation():
    iteration = 0
    now = datetime.now()
    current_date = now.strftime("%d.%m")
    bd_today = db_functions.name_and_group_get(current_date)
    last_congratulation_sent = await utils.get_congratulation_status()

    await app.send_message(chat_id, f"Статус {'Отправлено' if last_congratulation_sent == 1 else 'Не Отправлено'}")

    if bd_today and not last_congratulation_sent:
        await app.send_message(chat_id, "Сегодня кто-то родился, поздравление отправляется")
        num_images = -(-len(bd_today) // 3)
        for i in range(num_images):
            start_idx = i * 3
            end_idx = min((i + 1) * 3, len(bd_today))
            people_to_congratulate = bd_today[start_idx:end_idx]

            await birthday(app, group_id, chat_id, people_to_congratulate, iteration)
            iteration += 1
            await utils.save_congratulation_status(1)
    else:
        await app.send_message(chat_id, "Сегодня никто не родился (либо это перезапуск), поздравление не отправляется")

async def scheduler():
    await app.start()
    await app.send_message(chat_id, "Бот начал работу")

    last_congratulation_sent = await utils.get_congratulation_status()
    if not last_congratulation_sent:
        await send_congratulation()

    aioschedule.every().day.at("01:32").do(send_congratulation())

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



if __name__ == "__main__":
    asyncio.run(scheduler())
