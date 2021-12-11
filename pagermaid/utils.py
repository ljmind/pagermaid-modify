from os import remove
from sys import platform
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE

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


async def attach_log(plaintext, chat_id, file_name, reply_id=None, caption=None):
    """ Attach plaintext as logs. """
    file = open(file_name, "w+")
    file.write(plaintext)
    file.close()
    await bot.send_document(
        chat_id,
        file_name,
        reply_to_message_id=reply_id,
        caption=caption
    )
    remove(file_name)


async def execute(command, pass_error=True):
    """ Executes command and returns output, with the option of enabling stderr. """
    if not platform == 'win32':
        executor = await create_subprocess_shell(
            command,
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE
        )

        stdout, stderr = await executor.communicate()
        if pass_error:
            result = str(stdout.decode().strip()) \
                     + str(stderr.decode().strip())
        else:
            result = str(stdout.decode().strip())
    else:
        import subprocess
        subprocess.Popen('dir', shell=True)
        sub = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        sub.wait()
        stdout = sub.communicate()
        result = str(stdout[0].decode('gbk').strip())
    return result
