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
    SENIORS = ast.literal_eval(DATA_SERVER[4])

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
    if DATA_USER[15] == 0:
        builder.row(types.InlineKeyboardButton(text="🟢 Включить отчет ходока", callback_data="settings.onHodokForm"))
        USE_FORM_HODOK = '❌ Выключено'
    else:
        builder.row(types.InlineKeyboardButton(text="🔴 Выключить отчет ходока", callback_data="settings.offHodokForm"))
        USE_FORM_HODOK = '✅ Включено'
    if DATA_USER[18] == 0:
        builder.row(types.InlineKeyboardButton(text="🟢 Включить помощь", callback_data="settings.onHelp"))
        SETTINGS_HELP = '❌ Выключено'
    else:
        builder.row(types.InlineKeyboardButton(text="🔴 Выключить помощь", callback_data="settings.offHelp"))
        SETTINGS_HELP = '✅ Включена'
    builder.row(types.InlineKeyboardButton(text="🗂 Изменить шаблон", callback_data="settings.profiles"))
    builder.row(types.InlineKeyboardButton(text="📱 Настройка кнопок", callback_data="settings.buttons"))
    builder.row(types.InlineKeyboardButton(text="🗓 Выбрать смещение", callback_data="settings.smchange"))
    builder.row(types.InlineKeyboardButton(text="🗑 Очистка данных", callback_data="settings.clearMenu"))

    if DATA_USER[19] == -1:
        SENIOR_TEXT = 'Не установлено'
    else:
        SENIOR_TEXT = f'{SENIORS[DATA_USER[19]]}'

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ Настройки\n\n"
             f"🗂 Шаблон » {DATA_USER[13]}\n\n"
             f"⏰ Использовать секунды » {USE_SECOND}\n"
             f"📄 Отчет ходока в конце смены » {USE_FORM_HODOK}\n"
             f"🛟 Помощь » {SETTINGS_HELP}\n"
             f"😎 Твой старший » {SENIOR_TEXT}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())





@router.callback_query(F.data == 'settings.smchange')
async def smchange(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.smchange'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    USE_SECOND = ''

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="settings.Show"))
    builder.row(types.InlineKeyboardButton(text="Митя", callback_data="settings.setsm0"))
    builder.add(types.InlineKeyboardButton(text="Степа", callback_data="settings.setsm1"))
    builder.add(types.InlineKeyboardButton(text="Олег", callback_data="settings.setsm2"))
    builder.add(types.InlineKeyboardButton(text="Илья", callback_data="settings.setsm3"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 🗓 Выбрать смещение\n\n"
             f"Выбери своего старшего из предложенных вариантов",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'settings.setsm0')
async def setsm0(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await database.setUserID(message.from_user.id, 'sm', "'0'")
    await message.answer(
        text="✅ Установлено смещение!",
        show_alert=False
    )
    await Show(message, bot)


@router.callback_query(F.data == 'settings.setsm1')
async def setsm1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await database.setUserID(message.from_user.id, 'sm', "'1'")
    await message.answer(
        text="✅ Установлено смещение!",
        show_alert=False
    )
    await Show(message, bot)





@router.callback_query(F.data == 'settings.setsm2')
async def setsm2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await database.setUserID(message.from_user.id, 'sm', "'2'")
    await message.answer(
        text="✅ Установлено смещение!",
        show_alert=False
    )
    await Show(message, bot)




@router.callback_query(F.data == 'settings.setsm3')
async def setsm3(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await database.setUserID(message.from_user.id, 'sm', "'3'")
    await message.answer(
        text="✅ Установлено смещение!",
        show_alert=False
    )
    await Show(message, bot)






@router.callback_query(F.data == 'settings.clearMenu')
async def clearMenu(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.clearMenu'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    USE_SECOND = ''

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="settings.Show"))
    builder.row(types.InlineKeyboardButton(text="🗑 Очистить последних роботов", callback_data="settings.clearRobots"))
    builder.row(types.InlineKeyboardButton(text="🗑 Очистить последние маршруты", callback_data="settings.clearRoutes"))
    builder.row(types.InlineKeyboardButton(text="🗑 Очистить последние локации", callback_data="settings.clearLocations"))
    builder.row(types.InlineKeyboardButton(text="🗑 Очистить архив логов", callback_data="settings.clearLogs"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 🗑 Очистка данных",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'settings.buttons')
async def buttons(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttons'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    USE_SECOND = ''

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="settings.Show"))
    # builder.row(types.InlineKeyboardButton(text="➕ Добавить свою кнопку", callback_data="settings.none"))
    # builder.row(types.InlineKeyboardButton(text="❌ Удалить кнопку", callback_data="settings.none"))
    # builder.row(types.InlineKeyboardButton(text="📝 Редактировать кнопки", callback_data="settings.none"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    TEXT = ''
    BUTTONS = ast.literal_eval(DATA_USER[5])
    for button in BUTTONS:
        for button_info in button:
            button_info_get = await database.getData('actions', 'idGate', f"'{button_info}'")
            TEXT = f'{TEXT}<blockquote><b>{button_info_get[1]}</b> | {button_info_get[2]} | {button_info_get[3]}</blockquote>\n'

    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 📱 Настройка кнопок\n\n"
             f"📱 Текущий массив кнопок » {DATA_USER[5]}\n\nID КНОПКИ | НАЗВАНИЕ КНОПКИ | ТЕКСТ ДЛЯ ЛОГОВ"
             f"{TEXT}",
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
    ACTIONS = [['BASEACTION3'], ['BASEACTION16', 'BASEACTION17', 'BASEACTION18'], ['BASEACTION22'], ['BASEACTION19', 'BASEACTION20', 'BASEACTION21']]
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


@router.callback_query(F.data == 'settings.clearLocations')
async def clearLocations(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOTS_HISTORY = ast.literal_eval(DATA_USER[10])
    ROBOTS_HISTORY[2] = []

    await database.setUserID(message.from_user.id, 'logs_archive', f'"[]"')
    await message.answer(
        text="✅ Очищено!",
        show_alert=False
    )
    await Show(message, bot)


@router.callback_query(F.data == 'settings.clearLogs')
async def clearLogs(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOTS_HISTORY = []

    await database.setUserID(message.from_user.id, 'logs_archive', f'\"{ROBOTS_HISTORY}\"')
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


@router.callback_query(F.data == 'settings.onHodokForm')
async def onHodokForm(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await database.setUserID(message.from_user.id, 'settings_HodokForm', "'1'")
    await message.answer(
        text="✅ Включено",
        show_alert=False
    )
    await Show(message, bot)



@router.callback_query(F.data == 'settings.offHodokForm')
async def offHodokForm(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await database.setUserID(message.from_user.id, 'settings_HodokForm', "'0'")
    await message.answer(
        text="❌ Выключено",
        show_alert=False
    )
    await Show(message, bot)



@router.callback_query(F.data == 'settings.onHelp')
async def onHelp(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    if DATA_USER[19] == 0 or DATA_USER[19] == 2:
        await database.setUserID(message.from_user.id, 'settings_help', "'1'")
        await message.answer(
            text="✅ Включено",
            show_alert=False
        )
        await Show(message, bot)
    else:
        await message.answer(
            text="⚠️ Ошибка",
            show_alert=False
        )
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="settings.Show"))

        # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        MAIN = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"⚠️ Ошибка\n\n"
                 f"В данный момент помощь доступна только утренним сменам (1 и 2 смещение)\nВозможно у вас не установлено смещение, сделать это можно в настройках",
            message_id=DATA_USER[2],
            reply_markup=builder.as_markup())



@router.callback_query(F.data == 'settings.offHelp')
async def offHelp(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await database.setUserID(message.from_user.id, 'settings_help', "'0'")
    await message.answer(
        text="❌ Выключено",
        show_alert=False
    )
    await Show(message, bot)