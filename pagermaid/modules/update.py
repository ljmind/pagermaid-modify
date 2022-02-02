from pyrogram import Client

from pagermaid.listener import listener
from pagermaid.utils import lang, execute, Message, alias_command


@listener(is_plugin=False, outgoing=True, command=alias_command("update"),
          description=lang('update_des'),
          parameters="<true/debug>")
async def update(client: Client, message: Message):
    if len(message.parameter) > 1:
        await message.edit(lang('arg_error'))
        return
    await execute('git reset --hard HEAD')
    await execute('git pull')
    await message.edit(lang('update_success'))
    exit(1)
