from telethon import TelegramClient
import config as c
import asyncio
import modules
import logging
import os


class TelethonManager:

    def __init__(self, loop=None):
        self.loop = loop
        self.client = TelegramClient(session=c.SESSION_NAME, api_hash=c.API_HASH, api_id=c.API_ID, loop=self.loop)
        self.sources = dict()

        self.start()

    def start(self):

        ## register handlers
        modules.init(self.client, self.sources)

        ## register background events

        # Start
        self.client.start(bot_token=c.BOT_TOKEN)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    file_hand = logging.FileHandler("logging.log")
    file_hand.setLevel(logging.ERROR)
    logger.addHandler(file_hand)
    if not os.path.exists("buffer"):
        os.mkdir("buffer")
    TelethonManager()
