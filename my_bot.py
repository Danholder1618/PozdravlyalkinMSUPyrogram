import config
import utils
import text

from datetime import datetime, time, timedelta

# Отправка фотографии каждый день в 8 часов
async def birthday(app):
    await utils.make_image()
    photo_path = config.BG_PATH

    # Получение информации о текущем пользователе (боте)
    me = await app.get_me()

    # Какой-то там премиум
    if me is not None and hasattr(me, 'is_premium'):
        file_size_limit_mib = 4000 if me.is_premium else 2000
    else:
        file_size_limit_mib = 2000

    message = await app.send_photo(config.MSU_ID, photo_path, text.podpis)
    message_id = message.id

    await utils.save_congratulation_status(1)
    last_congratulation_sent = await utils.get_congratulation_status()
    await app.send_message(config.MY_ID, f"Статус {'Отправлено' if last_congratulation_sent == 1 else 'Не Отправлено'}")

    # Рассчитываем время следующего выполнения (3:59 утра следующего дня)
    now = datetime.now()
    next_run = datetime.combine(now.date() + timedelta(days=1), time(3, 59))
    delay = (next_run - now).total_seconds()

    hours, remainder = divmod(delay, 3600)
    minutes, seconds = divmod(remainder, 60)

    await app.send_message(config.MY_ID,
                           f"!Поздравление отправлено, уделение будет через: {int(hours)} часов, {int(minutes)} минут, {int(seconds)} секунд.")
    await utils.save_message_id(message_id)
    await utils.delete_message(config.MY_ID, delay, app)
