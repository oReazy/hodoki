import asyncio, logging, time, states, ast

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types, html, F, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database, mainMenu

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

router = Router()

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

async def registation_0(message: types.Message, bot: Bot):
    DATA_SERVER = await database.getData('settings', 'id', "'1'") # Получаем данные сервера
    await database.addNewAccount(message.from_user.id)
    NEW_MESSAGE = await bot.send_message(
        chat_id=message.from_user.id,
        text='📶 Подключаемся к боту...'
    )
    await database.setUserID(message.from_user.id, "tg_mainMessage", f"'{NEW_MESSAGE.message_id}'")
    await registration_1(message, bot)

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

@router.callback_query(F.data == 'registration.registration_1')
async def registration_1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'registration.registration_1_check'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"👋 Добро пожаловать в <b>{DATA_SERVER[1]}</b>\n\n"
             f"📝 Для того, чтобы продолжить, введите проверочный код",
        message_id=DATA_USER[2],
    )


@router.callback_query(F.data == 'registration.registration_1_check')
async def registration_1_check(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'registration.registration_1_check'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    if message.text == DATA_SERVER[2]:
        await mainMenu.Show(message, bot)
    else:
        MAIN = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"👋 Добро пожаловать в <b>{DATA_SERVER[1]}</b>\n\n"
                 f"❌ Вы ввели неверный проверочный код!\n\n"
                 f"📝 Для того, чтобы продолжить, введите проверочный код",
            message_id=DATA_USER[2],
        )