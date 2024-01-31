import pyrogram
import asyncio
import config
import db_functions
import time as stime

from pyrogram import Client
from my_bot import birthday
from datetime import datetime, time, timedelta

async def main():
    app = Client("Поздравлялкин Тестовый", api_id=config.APP_API_ID, api_hash=config.APP_API_HASH, bot_token=config.T_T)
    await app.start()

    # Создаем событие для синхронизации
    shutdown_event = asyncio.Event()

    async def scheduled():
        while not shutdown_event.is_set():
            now = datetime.now()
            if now.time() >= time(8, 0):
                current_date = datetime.now().strftime("%d.%m")
                current_date = "'" + current_date + "'"
                bd_tuday = db_functions.name_and_group_get(current_date)
                if len(bd_tuday) != 0:
                    await birthday(app)

                await asyncio.sleep(60)

    await asyncio.create_task(scheduled())
    await asyncio.Event().wait()

    # Ожидание события завершения
    await shutdown_event.wait()

    # Завершение приложения
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
