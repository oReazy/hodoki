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


@router.callback_query(F.data == 'lastlog.Show')
async def Show(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'lastlog.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="mainMenu.Show"))
    builder.row(types.InlineKeyboardButton(text="📄 Скопировать", callback_data="none"))

    LOGS = ast.literal_eval(DATA_USER[7])

    TEXT_LOGS = ''
    for item in LOGS[0][:-1]:
        TEXT_LOGS = f"{TEXT_LOGS}\n{item}"

    TEXT_BOT_INFO = ''
    if LOGS[0][-1][0] != 0:
        TEXT_BOT_INFO = f'🤖 <b>А{LOGS[0][-1][0]}</b>'
    if LOGS[0][-1][1] != 0:
        TEXT_BOT_INFO = f'{TEXT_BOT_INFO} • 🗺 <b>Маршрут {LOGS[0][-1][1]}</b>\n'
    else:
        TEXT_BOT_INFO = f'{TEXT_BOT_INFO}\n'

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 📄 Последний лог\n\n"
             f"{TEXT_BOT_INFO}"
             f"{TEXT_LOGS}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
