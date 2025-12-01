
import asyncio, logging, time, states

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types, html, F, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

async def logoutServer(bot: Bot):
    TIME= int(time.time())
    TIME_TASK = TIME - 28800
    USERS = await database.getMultiProgramBdData('users', f"tg_lastMessage < {TIME_TASK} AND tg_online = 1")
    for USER in USERS:
        await database.setUserID(f'{USER[1]}', 'tg_online', "'0'")
        await bot.delete_message(
            chat_id=USER[1],
            message_id=USER[2]
        )
        await bot.send_message(
            chat_id=USER[1],
            text='❇️ Чтобы продолжить, напишите /start'
        )
