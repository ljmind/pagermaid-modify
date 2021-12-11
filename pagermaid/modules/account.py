from os import remove, sep
from struct import error as StructError

from pyrogram import Client
from pyrogram.types import User, Chat

from pagermaid import bot
from pagermaid.listener import listener
from pagermaid.utils import lang, Message


class Profile:
    def __init__(self, message: Message):
        if len(message.text.split()) == 2:
            user = message.text.split()[1].replace("@", "")
            if user.isnumeric():
                user = int(user)
            try:
                self.member = bot.get_users(user)
            except IndexError:
                self.member = bot.get_chat(user)
            except (TypeError, ValueError, OverflowError, StructError) as exception:
                if str(exception).startswith("Cannot find any entity corresponding to"):
                    message.edit("出错了呜呜呜 ~ 指定的用户不存在。")
                    return
                if str(exception).startswith("No user has"):
                    message.edit("出错了呜呜呜 ~ 指定的道纹不存在。")
                    return
                if str(exception).startswith("Could not find the input entity for") or isinstance(exception,
                                                                                                  StructError):
                    message.edit("出错了呜呜呜 ~ 无法通过此 UserID 找到对应的用户。")
                    return
                if isinstance(exception, OverflowError):
                    message.edit("出错了呜呜呜 ~ 指定的 UserID 已超出长度限制，您确定输对了？")
                    return
                raise exception
            self.user = True if isinstance(self.member, User) else False
            self.chat = True if isinstance(self.member, Chat) else False
        elif message.entities is not None:
            if message.mentioned:
                self.user = True
                self.member = message.entities[0].user
            else:
                self.user = True if isinstance(message.from_user, User) else False
                self.chat = True if isinstance(message.sender_chat, Chat) else False
                self.member = message.from_user if message.from_user else message.sender_chat
                if not self.member:
                    self.member = message.chat
        else:
            self.user = True if isinstance(message.from_user, User) else False
            self.chat = True if isinstance(message.sender_chat, Chat) else False
            self.member = message.from_user if message.from_user else message.sender_chat
            if not self.member:
                self.member = message.chat
        self.id = self.member.id
        self.is_bot = self.member.is_bot if self.user else False
        self.first_name = self.member.first_name.replace("\u2060", "") if (self.user and self.member.first_name) else ""
        self.last_name = self.member.last_name.replace("\u2060", "") if (self.user and self.member.last_name) else ""
        self.name = self.member.first_name + self.last_name if self.user else self.member.title
        self.username = self.member.username
        self.dc_id = self.member.dc_id
        self.is_verified = self.member.is_verified
        self.is_restricted = self.member.is_restricted
        self.mention = self.member.mention if self.user else None
        self.mention = f"[{self.name}](https://t.me/{self.username})" if (self.chat and self.username) else self.mention


@listener(is_plugin=False, command='profile',
          description=lang('profile_des'),
          parameters="<username>")
async def profile(client: Client, message: Message):
    """ Queries profile of a user. """
    if len(message.text.split()) > 2:
        await message.edit("出错了呜呜呜 ~ 无效的参数。")
        return

    await message.edit("正在生成用户简介摘要中 . . .")
    reply = message.reply_to_message
    if reply:
        target_user = Profile(reply)
    else:
        target_user = Profile(message)
    user_type = "Bot" if target_user.is_bot else ("用户" if target_user.user else "会话")
    username_system = f"@{target_user.username}" if target_user.username is not None else (
        "喵喵喵 ~ 好像没有设置")
    first_name = target_user.first_name if target_user.first_name else "喵喵喵 ~ 好像没有设置"
    last_name = target_user.last_name if target_user.last_name else "喵喵喵 ~ 好像没有设置"
    verified = "是" if target_user.is_verified else "否"
    restricted = "是" if target_user.is_restricted else "否"
    caption = f"**用户简介:** \n" \
              f"道纹: {username_system} \n" \
              f"ID: `{target_user.id}` \n" \
              f"名字: {first_name} \n" \
              f"姓氏: {last_name} \n" \
              f"官方认证: {verified} \n" \
              f"受限制: {restricted} \n" \
              f"类型: {user_type} \n" \
              f"{target_user.mention}"
    try:
        photo = await bot.get_profile_photos(target_user.id, limit=1)
        photo = await bot.download_media(photo[0].file_id, 'photo.jpg')
    except:
        pass
    try:
        try:
            await bot.send_photo(
                message.chat.id,
                f'downloads{sep}photo.jpg',
                caption=caption,
                reply_to_message_id=reply.message_id if reply else None
            )
            await message.delete()
            try:
                remove(photo)  # noqa
            except:
                pass
            return
        except TypeError:
            await message.edit(caption)
    except:
        try:
            await bot.send_photo(
                message.chat.id,
                f'downloads{sep}photo.jpg',
                caption=caption
            )
            await message.delete()
            try:
                remove(photo)
            except:
                pass
            return
        except TypeError:
            await message.edit(caption)
