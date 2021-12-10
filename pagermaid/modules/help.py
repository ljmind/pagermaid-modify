""" The help module. """
from pyrogram import Client

from os import listdir
from pagermaid import help_messages, Config
from pagermaid.utils import lang, Message
from pagermaid.listener import listener


@listener(is_plugin=False, command="help",
          description=lang('help_des'),
          parameters=f"<{lang('command')}>")
async def help_command(client: Client, message: Message):
    """ The help new command,"""
    support_commands = ['username', 'name', 'pfp', 'bio', 'rmpfp',
                        'profile', 'block', 'unblock', 'ghost', 'deny', 'convert',
                        'caption', 'ocr', 'highlight', 'time', 'translate',
                        'tts', 'google', 'animate',
                        'teletype', 'widen', 'owo', 'flip',
                        'rng', 'aaa', 'tuxsay', 'coin', 'help',
                        'lang', 'alias', 'id', 'uslog', 'log',
                        're', 'leave', 'hitokoto', 'apt', 'prune', 'selfprune',
                        'yourprune', 'del', 'genqr', 'parseqr',
                        'sb', 'sysinfo', 'status',
                        'stats', 'speedtest', 'connection',
                        'pingdc', 'ping', 'topcloud',
                        's', 'sticker', 'sh', 'restart',
                        'trace', 'chat', 'update']
    if message.arguments:
        if message.arguments in help_messages:
            await message.edit(str(help_messages[message.arguments]))
        else:
            await message.edit(lang('arg_error'))
    else:
        result = f"**{lang('help_list')}: \n**"
        for command in sorted(help_messages, reverse=False):
            if str(command) in support_commands:
                continue
            result += "`" + str(command)
            result += "`, "
        if result == f"**{lang('help_list')}: \n**":
            """ The help raw command,"""
            for command in sorted(help_messages, reverse=False):
                result += "`" + str(command)
                result += "`, "
        await message.edit(result[:-2] + f"\n**{lang('help_send')} \"!help <{lang('command')}>\" {lang('help_see')}**\n"
                                         f"[{lang('help_source')}](https://t.me/PagerMaid_Modify) "
                                         f"[{lang('help_plugin')}](https://index.xtaolabs.com/) "
                                         f"[{lang('help_module')}](https://wiki.xtaolabs.com/)",
                           disable_web_page_preview=True)


@listener(is_plugin=False, command="help_raw",
          description=lang('help_des'),
          parameters=f"<{lang('command')}>")
async def help_raw_command(client: Client, message: Message):
    """ The help raw command,"""
    if message.arguments:
        if message.arguments in help_messages:
            await message.edit(str(help_messages[message.arguments]))
        else:
            await message.edit(lang('arg_error'))
    else:
        result = f"**{lang('help_list')}: \n**"
        for command in sorted(help_messages, reverse=False):
            result += "`" + str(command)
            result += "`, "
        await message.edit(result[:-2] + f"\n**{lang('help_send')} \"-help <{lang('command')}>\" {lang('help_see')}** "
                                         f"[{lang('help_source')}](https://t.me/PagerMaid_Modify)",
                           disable_web_page_preview=True)


@listener(is_plugin=False, command="lang",
          description=lang('lang_des'))
async def lang_change(client: Client, message: Message):
    to_lang = message.arguments
    from_lang = Config.LANGUAGE
    dir_, dir__ = listdir('languages/built-in'), []
    for i in dir_:
        if not i.find('yml') == -1:
            dir__.append(i[:-4])
    with open('config.yml') as f:
        file = f.read()
    if to_lang in dir__:
        file = file.replace(f'application_language: "{from_lang}"', f'application_language: "{to_lang}"')
        with open('config.yml', 'w') as f:
            f.write(file)
        await message.edit(f"{lang('lang_change_to')} {to_lang}, {lang('lang_reboot')}")
        exit(1)
    else:
        await message.edit(
            f'{lang("lang_current_lang")} {Config.LANGUAGE}\n\n{lang("lang_all_lang")}{"，".join(dir__)}')
