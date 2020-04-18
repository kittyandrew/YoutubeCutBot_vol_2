from utils.downloader import download_by_url
from telethon.events import StopPropagation
from telethon.utils import get_attributes
from telethon.tl.custom import Message
from utils.cutter import cut_the_butt
from telethon import events
from typing import Union
import secrets
import re
import os
Event = Union[Message, events.NewMessage.Event]


def links_extractor(text):
    raw_url_pattern = r""
    url_pattern = re.compile(raw_url_pattern)
    return url_pattern.findall(text)


async def init(bot, sources):
    @bot.on(events.NewMessage(pattern="^/(start|new|link).*?$"))
    async def start_handler(event:Event):
        await event.reply("Please send me source (link):\n"
                          "`https://link.to.youtube.vid`")
        sources[event.chat_id] = "Waiting for source"
        raise StopPropagation()

    @bot.on(events.NewMessage(func=lambda e: sources.get(e.chat_id, "") == "Waiting for source"))
    async def start_handler(event: Event):
        if event.text:
            sources[event.chat_id] = event.text
            await event.reply(f"Great, source added:```{event.text}```Now add time stamps\n"
                              f"(format -- `3:04-4:09, 5:28-7:00 8:11-8:12` -- comma or space separated)")

    @bot.on(events.NewMessage(pattern=r"\d{1,3}\:\d\d\-\d{1,3}\:\d\d"))
    async def url_handler(event: Event):
        client = event.client

        link = sources.get(event.chat_id, None)
        if not link:
            await event.reply("You must add source first!")
            return

        real_path = os.path.join("buffer", f"folder_{secrets.token_urlsafe(16)}")
        os.mkdir(real_path)

        await download_by_url(link, real_path)

        try:
            # Finding all downloaded videos in the current directory
            for path in [f for f in os.listdir(real_path) if os.path.isfile(os.path.join(real_path, f))]:
                path = os.path.join(real_path, path)
                # Cutting Magic
                cutted_paths = cut_the_butt(path, event.text)

                try:
                    for cutted_path in cutted_paths:
                        # Uploading file to telegram servers with telethon
                        file = await client.upload_file(
                            cutted_path
                        )

                        # Getting attributes of the uploaded file
                        try:
                            attributes = get_attributes(cutted_path)[0]
                        except Exception as e:
                            attributes = None

                        # Make sure deletion of your message is not raising
                        try:
                            await client.send_file(
                                event.chat_id,
                                file,
                                attributes=attributes,
                                reply_to=event,
                                #force_document=True
                            )
                        except:
                            await client.send_file(
                                event.chat_id,
                                file,
                                attributes=attributes,
                                #force_document=True
                            )

                finally:
                    # Finally remove downloaded file
                    os.remove(path)
                    for _path in cutted_paths:
                        os.remove(_path)
        finally:
            # Finally delete empty folder
            os.rmdir(real_path)



