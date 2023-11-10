from pyrogram import filters
from pyrogram.types import Message
from main import app

import text

@app.on_message(filters.command("start"))
def start_command(client, message):
    chat_id = message.chat.id
    client.send_message(chat_id, text.greet)