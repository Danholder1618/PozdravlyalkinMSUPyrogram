import config
import utils
import text

from datetime import datetime, time, timedelta

# Отправка фотографии каждый день в 8 часов
async def birthday(app):
    chat_id = config.CHAT_ID
    await utils.make_image()
    photo_path = config.BG_PATH

    # Получение информации о текущем пользователе (боте)
    me = await app.get_me()

    # Какой-то там премиум
    if me is not None and hasattr(me, 'is_premium'):
        file_size_limit_mib = 4000 if me.is_premium else 2000
    else:
        file_size_limit_mib = 2000

    message = await app.send_photo(chat_id, photo_path, text.podpis)
    message_id = message.id

    # Рассчитываем время следующего выполнения (8 утра следующего дня)
    now = datetime.now()
    next_run = datetime.combine(now.date() + timedelta(days=1), time(7, 59))
    delay = (next_run - now).total_seconds()

    await utils.save_message_id(str(message_id))
    await utils.delete_message(chat_id, message_id, delay, app)
