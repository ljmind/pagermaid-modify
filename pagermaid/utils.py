from os import remove
from pyrogram.types import Message
from pagermaid.config import Config
from pagermaid import bot


class Message(Message):  # noqa
    arguments: str


def lang(text: str) -> str:
    """ i18n """
    result = Config.lang_dict.get(text, text)
    return result


async def attach_report(plaintext, file_name, reply_id=None, caption=None):
    """ Attach plaintext as logs. """
    file = open(file_name, "w+")
    file.write(plaintext)
    file.close()
    try:
        await bot.send_document(
            "PagerMaid_Modify_bot",
            file_name,
            reply_to_message_id=reply_id,
            caption=caption
        )
    except:
        return
    remove(file_name)
