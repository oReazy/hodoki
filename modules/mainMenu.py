import asyncio, logging, time, states, ast

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types, html, F, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

router = Router()

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————


@router.callback_query(F.data == 'mainMenu.Show')
async def Show(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'mainMenu.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🟩 Начать запись", callback_data="record.StartRobot"))
    builder.row(types.InlineKeyboardButton(text="📄 Последний лог", callback_data="lastlog.Show"))
    # builder.add(types.InlineKeyboardButton(text="📑 Архив логов", callback_data="none"))
    builder.row(types.InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings.Show"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 Главное меню",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
