from telethon import events
from telethon.sync import TelegramClient
from help import TeleScraper
from db_funcs import MyDb
import os


api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# We have to manually call "start" if we want an explicit bot token
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)
my_db = MyDb("posts_db")


@bot.on(events.NewMessage)
async def my_event_handler(event):
    if "t.me/" in event.raw_text:

        sender_id = event.sender.id
        data = TeleScraper(event.raw_text)
        await data.run()

        save_data = (
            sender_id,
            data.content,
            data.media_data,
            data.author,
            data.dateTime,
            event.raw_text,
        )
        my_db.save_to_db(save_data)

        await event.reply(data.content)


bot.start()
bot.run_until_disconnected()
