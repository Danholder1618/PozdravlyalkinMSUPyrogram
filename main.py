import pyrogram
import asyncio
import config
import sched
import db_functions
import time as stime

from pyrogram import Client
from my_bot import birthday
from datetime import datetime, time

async def main():
    app = Client("Поздравлялкин", api_id=config.APP_API_ID, api_hash=config.APP_API_HASH, bot_token=config.BOT_TOKEN)
    scheduler = sched.scheduler(stime.time, stime.sleep)

    # Создаем событие для синхронизации
    shutdown_event = asyncio.Event()

    async def scheduled():
        await app.start()
        now = datetime.now()
        if now.time() >= time(8, 0):
            current_date = datetime.now().strftime("%d.%m")
            current_date = "'" + current_date + "'"
            bd_tuday = db_functions.name_and_group_get(current_date)
            if len(bd_tuday) != 0:
                await birthday(app)

        # Планировщик для следующего выполнения
        next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)  # Установка времени следующего выполнения
        if next_run < now:
            next_run = next_run.replace(day=next_run.day + 1)  # Если текущее время > 8:00, то перенести на следующий день

        # Задержка до следующего выполнения
        delay = (next_run - now).total_seconds()

        # Планирование следующего выполнения
        loop.call_later(delay, lambda: asyncio.create_task(scheduled()))

    # Запуск планировщика
    loop = asyncio.get_event_loop()
    loop.call_later(0, lambda: asyncio.create_task(scheduled()))

    # Ожидание события завершения
    await shutdown_event.wait()

    # Завершение приложения
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
