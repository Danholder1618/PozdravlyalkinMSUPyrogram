from pyrogram import filters
from main import app

import text

@app.on_message(filters.command("start"))
def start_command(client, message):
    client.send_message(message.chat.id, text.greet)