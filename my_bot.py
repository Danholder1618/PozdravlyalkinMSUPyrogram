import config
import utils
import text

from datetime import datetime, time, timedelta

# Отправка фотографии каждый день в 8 часов
async def birthday(app, group_id, chat_id, people_to_congratulate, iteration):
    await utils.make_image(people_to_congratulate)
    photo_path = config.BG_PATH

    # Получение информации о текущем пользователе (боте)
    me = await app.get_me()

    # Какой-то там премиум
    if me is not None and hasattr(me, 'is_premium'):
        file_size_limit_mib = 4000 if me.is_premium else 2000
    else:
        file_size_limit_mib = 2000

    # Удаление прошлой фотографии
    if (iteration == 0): await utils.delete_message(chat_id, group_id, app)

    # Отправка новой фотографии
    message = await app.send_photo(group_id, photo_path, text.podpis)
    message_id = message.id

    await utils.save_congratulation_status(1)
    last_congratulation_sent = await utils.get_congratulation_status()
    await app.send_message(config.MY_ID, f"Статус {'Отправлено' if last_congratulation_sent == 1 else 'Не Отправлено'}")

    await utils.save_message_id(message_id)
