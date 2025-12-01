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


@router.callback_query(F.data == 'settings.Show')
async def Show(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    USE_SECOND = ''

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="mainMenu.Show"))
    if DATA_USER[9] == 0:
        builder.row(types.InlineKeyboardButton(text="🟢 Включить секунды", callback_data="settings.onSeconds"))
        USE_SECOND = '❌ Выключено'
    else:
        builder.row(types.InlineKeyboardButton(text="🔴 Выключить секунды", callback_data="settings.offSeconds"))
        USE_SECOND = '✅ Включено'
    builder.row(types.InlineKeyboardButton(text="🗂 Изменить шаблон", callback_data="settings.profiles"))
    builder.row(types.InlineKeyboardButton(text="🗑 Очистить последних роботов", callback_data="settings.clearRobots"))
    builder.row(types.InlineKeyboardButton(text="🗑 Очистить последние маршруты", callback_data="settings.clearRoutes"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ Настройки\n\n"
             f"⏰ Использовать секунды » {USE_SECOND}\n"
             f"🗂 Шаблон » {DATA_USER[13]}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'settings.profiles')
async def profiles(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.profiles'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    USE_SECOND = ''

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="settings.Show"))
    builder.row(types.InlineKeyboardButton(text="🤖 Использовать МЛП", callback_data="settings.profilesMLP"))
    builder.row(types.InlineKeyboardButton(text="🤖 Использовать МЛП (минимал)", callback_data="settings.profilesMLPMin"))
    builder.row(types.InlineKeyboardButton(text="🏃‍➡️ Использовать ходоковский", callback_data="settings.profilesHodok"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 🗂 Изменить шаблон\n\n"
             f"🗂 Шаблон » {DATA_USER[13]}\n\n"
             f"Шаблоны — это готовый пресет кнопок и функций для комфортной работы в выбранной задаче. В данный момент есть два готовых шаблона: МЛП и ходоковские",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'settings.profilesMLP')
async def profilesMLP(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.profiles'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ACTIONS = [['BASEACTION1'], ['BASEACTION2', 'BASEACTION3'], ['BASEACTION4', 'BASEACTION5'], ['BASEACTION6'], ['BASEACTION7'], ['BASEACTION8'], ['BASEACTION9'], ['BASEACTION10'], ['BASEACTION11'], ['BASEACTION12', 'BASEACTION13', 'BASEACTION14'], ['BASEACTION15'], ['BASEACTION16', 'BASEACTION17', 'BASEACTION18']]
    await database.setUserID(message.from_user.id, 'actions', f'\"{ACTIONS}\"')
    await database.setUserID(message.from_user.id, 'profile', f"'МЛП'")
    await message.answer(
        text="✅ Установлен новый шаблон",
        show_alert=False
    )
    await profiles(message, bot)


@router.callback_query(F.data == 'settings.profilesMLPMin')
async def profilesMLPMin(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.profiles'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ACTIONS = [['BASEACTION1'], ['BASEACTION2', 'BASEACTION3'], ['BASEACTION4', 'BASEACTION5'], ['BASEACTION6'], ['BASEACTION7'], ['BASEACTION8'], ['BASEACTION9'], ['BASEACTION10'], ['BASEACTION11'], ['BASEACTION12', 'BASEACTION13', 'BASEACTION14'], ['BASEACTION15']]
    await database.setUserID(message.from_user.id, 'actions', f'\"{ACTIONS}\"')
    await database.setUserID(message.from_user.id, 'profile', f"'МЛП (уменьшенный)'")
    await message.answer(
        text="✅ Установлен новый шаблон",
        show_alert=False
    )
    await profiles(message, bot)


@router.callback_query(F.data == 'settings.profilesHodok')
async def profilesHodok(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.profiles'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ACTIONS = [['BASEACTION3'], ['BASEACTION16', 'BASEACTION17', 'BASEACTION18'], ['BASEACTION19', 'BASEACTION20', 'BASEACTION21']]
    await database.setUserID(message.from_user.id, 'actions', f'\"{ACTIONS}\"')
    await database.setUserID(message.from_user.id, 'profile', f"'Ходок'")
    await message.answer(
        text="✅ Установлен новый шаблон",
        show_alert=False
    )
    await profiles(message, bot)


@router.callback_query(F.data == 'settings.clearRoutes')
async def clearRoutes(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOTS_HISTORY = ast.literal_eval(DATA_USER[10])
    ROBOTS_HISTORY[1] = []

    await database.setUserID(message.from_user.id, 'robot_info_archive', f'\"{ROBOTS_HISTORY}\"')
    await message.answer(
        text="✅ Очищено!",
        show_alert=False
    )
    await Show(message, bot)


@router.callback_query(F.data == 'settings.clearRobots')
async def clearRobots(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOTS_HISTORY = ast.literal_eval(DATA_USER[10])
    ROBOTS_HISTORY[0] = []

    await database.setUserID(message.from_user.id, 'robot_info_archive', f'\"{ROBOTS_HISTORY}\"')
    await message.answer(
        text="✅ Очищено!",
        show_alert=False
    )
    await Show(message, bot)



@router.callback_query(F.data == 'settings.onSeconds')
async def onSeconds(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await database.setUserID(message.from_user.id, 'settingTimeAdd', "'1'")
    await message.answer(
        text="✅ Включено",
        show_alert=False
    )
    await Show(message, bot)



@router.callback_query(F.data == 'settings.offSeconds')
async def offSeconds(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await database.setUserID(message.from_user.id, 'settingTimeAdd', "'0'")
    await message.answer(
        text="❌ Выключено",
        show_alert=False
    )
    await Show(message, bot)