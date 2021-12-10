""" PagerMaid module that contains utilities related to system status. """
from datetime import datetime
from platform import uname, python_version
from sys import platform

from pyrogram import Client, __version__

from pagermaid import start_time, Config
from pagermaid.listener import listener
from pagermaid.utils import lang, Message


@listener(is_plugin=False, command="status",
          description=lang('status_des'))
async def status(client: Client, message: Message):
    # database
    # database = lang('status_online') if redis_status() else lang('status_offline')
    # uptime https://gist.github.com/borgstrom/936ca741e885a1438c374824efb038b3
    time_units = (
        ('%m', 60 * 60 * 24 * 30),
        ('%d', 60 * 60 * 24),
        ('%H', 60 * 60),
        ('%M', 60),
        ('%S', 1)
    )

    async def human_time_duration(seconds):
        parts = {}
        for unit, div in time_units:
            amount, seconds = divmod(int(seconds), div)
            parts[unit] = str(amount)
        time_form = Config.START_FORM
        for key, value in parts.items():
            time_form = time_form.replace(key, value)
        return time_form

    current_time = datetime.utcnow()
    uptime_sec = (current_time - start_time).total_seconds()
    uptime = await human_time_duration(int(uptime_sec))
    text = (f"**{lang('status_hint')}** \n"
            f"{lang('status_name')}: `{uname().node}` \n"
            f"{lang('status_platform')}: `{platform}` \n"
            f"{lang('status_release')}: `{uname().release}` \n"
            f"{lang('status_python')}: `{python_version()}` \n"
            f"{lang('status_pyrogram')}: `{__version__}` \n"
            f"{lang('status_uptime')}: `{uptime}`"
            )
    await message.edit(text)
