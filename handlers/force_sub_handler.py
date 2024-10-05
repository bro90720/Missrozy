# (c) @LazyDeveloperr

import asyncio
from typing import (
    Union
)
from configs import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def get_invite_link(bot: Client, chat_id: Union[str, int]):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        print(f"Sleep of {e.value}s caused by FloodWait ...")
        await asyncio.sleep(e.value)
        return await get_invite_link(bot, chat_id)


async def handle_force_sub(bot: Client, cmd: Message):
    if Config.UPDATES_CHANNEL and Config.UPDATES_CHANNEL.startswith("-100"):
        channel_chat_id = int(Config.UPDATES_CHANNEL)
    elif Config.UPDATES_CHANNEL and (not Config.UPDATES_CHANNEL.startswith("-100")):
        channel_chat_id = Config.UPDATES_CHANNEL
    else:
        return 200
    try:
        user = await bot.get_chat_member(chat_id=channel_chat_id, user_id=cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="Sᴏʀʀʏ ʙᴀʙʏ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴍᴇ [Contact Me](https://t.me/sadspirit7).",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        try:
            invite_link = await get_invite_link(bot, chat_id=channel_chat_id)
        except Exception as err:
            print(f"Uɴᴀʙʟᴇ Tᴏ Dᴏ Fᴏʀᴄᴇ Sᴜʙsᴄʀɪʙᴇ Tᴏ {Config.UPDATES_CHANNEL}\n\nError: {err}")
            return 200
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Pʟᴇᴀsᴇ Jᴏɪɴ Mʏ Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Tʜɪs Bᴏᴛ**\n\n"
                 "Dᴜᴇ Tᴏ Pʀɪᴠᴀᴄʏ, Oɴʟʏ Cʜᴀɴɴᴇʟ Sᴜʙsᴄʀɪʙᴇʀs Usᴇ Tʜɪs Bᴏᴛ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Jᴏɪɴ Cʜᴀɴɴᴇʟ", url=invite_link.invite_link)
                    ],
                    [
                        InlineKeyboardButton("Rᴇғʀᴇsʜ", callback_data="refreshForceSub")
                    ]
                ]
            )
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="Sᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ Cᴏɴᴛᴀᴄᴛ Mʏ [Sᴘɪʀɪᴛs Cʜᴀᴛ Gʀᴏᴜᴘ](https://t.me/anime_help_group).",
            disable_web_page_preview=True
        )
        return 200
    return 200

