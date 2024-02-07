import pyrogram
import asyncio
import config
import db_functions
import time as stime
import utils

from pyrogram import Client
from my_bot import birthday
from datetime import datetime, time, timedelta

async def main():
    app = Client("Поздравлялкин", api_id=config.APP_API_ID, api_hash=config.APP_API_HASH, bot_token=config.BOT_TOKEN)
    await app.start()

    # Создаем событие для синхронизации
    shutdown_event = asyncio.Event()

    async def scheduled():
        while not shutdown_event.is_set():
            now = datetime.now()

            # Получение статуса отправки последнего поздравления
            last_congratulation_sent = await utils.get_congratulation_status()

            if now.time() >= time(8, 0):
                current_date = datetime.now().strftime("%d.%m")
                current_date = "'" + current_date + "'"
                bd_tuday = db_functions.name_and_group_get(current_date)

                await app.send_message(config.MY_ID, f"Статус {'Отправлено' if last_congratulation_sent == 1 else 'Не Отправлено'}")

                if ((len(bd_tuday) != 0) and (last_congratulation_sent == 0)):
                    await app.send_message(config.MY_ID, "!Сегодня кто-то родился, поздравление отправляется")
                    await birthday(app)
                else:
                    now = datetime.now()
                    next_run = datetime.combine(now.date() + timedelta(days=1), time(7, 59))
                    delay = (next_run - now).total_seconds()

                    hours, remainder = divmod(delay, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    await app.send_message(config.MY_ID,
                                           f"!Сегодня никто не родился (либо это перезапуск), поздравление будет через: {int(hours)} часов, {int(minutes)} минут, {int(seconds)} секунд.")
                    await asyncio.sleep(delay)

                delay = 70
                await app.send_message(config.MY_ID, f"!Поздравление было удалено, следующее через: {delay} секунд")
                await utils.save_congratulation_status(0)
                await app.send_message(config.MY_ID, f"Статус {'Отправлено' if last_congratulation_sent == 1 else 'Не Отправлено'}")
                await asyncio.sleep(delay)

    await asyncio.create_task(scheduled())
    await asyncio.Event().wait()

    # Ожидание события завершения
    await shutdown_event.wait()

    # Завершение приложения
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
