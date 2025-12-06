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


@router.callback_query(F.data == 'archive.Show')
async def Show(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'archive.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)
    ARCHIVE = ast.literal_eval(DATA_USER[7])

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="mainMenu.Show"))
    count = 0
    for item in ARCHIVE:
        builder.row(types.InlineKeyboardButton(text=f"🤖 {item[-1][0]} • 🗺 {item[-1][1]} • {item[-1][2]}", callback_data=f"archive.ShowLogs-{count}"))
        count = count + 1

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 📑 Архив логов",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())




@router.callback_query(F.data.startswith('archive.ShowLogs-'))
async def Show(callback: types.CallbackQuery, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(callback.from_user.id, "tg_answer", "'0'")
    await database.setUserID(callback.from_user.id, "state", "'archive.Show'")
    DATA_USER = await database.getUserID(callback.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="archive.Show"))

    LOGS = ast.literal_eval(DATA_USER[7])
    IDLOG = callback.data.replace('archive.ShowLogs-', '')
    IDLOG = int(IDLOG)
    TEXT_LOGS = ''
    for item in LOGS[IDLOG][:-1]:
        TEXT_LOGS = f"{TEXT_LOGS}\n{item}"

    TEXT_BOT_INFO = ''
    if LOGS[IDLOG][-1][0] != 0:
        TEXT_BOT_INFO = f'🤖 <b>А{LOGS[IDLOG][-1][0]}</b>'
    if LOGS[IDLOG][-1][1] != 0:
        TEXT_BOT_INFO = f'{TEXT_BOT_INFO} • 🗺 <b>{LOGS[IDLOG][-1][1]}</b>\n'
    else:
        TEXT_BOT_INFO = f'{TEXT_BOT_INFO}\n'

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=callback.from_user.id,
        text=f"🎯 » 📄 » Архивный лог\n\n"
             f"{TEXT_BOT_INFO}"
             f"{TEXT_LOGS}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
