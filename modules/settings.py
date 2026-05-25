import asyncio, logging, time, states, ast
import random

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
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="mainMenu.Show", icon_custom_emoji_id='5220091062441251597'))
    if DATA_USER[9] == 0:
        builder.row(types.InlineKeyboardButton(text="Cекунды", callback_data="settings.onSeconds", icon_custom_emoji_id='5219885475241691837'))
        USE_SECOND = '❌ Выключено'
    else:
        builder.row(types.InlineKeyboardButton(text="Cекунды", callback_data="settings.offSeconds", icon_custom_emoji_id='5219791114810199158', style='success'))
        USE_SECOND = '✅ Включено'
    if DATA_USER[15] == 0:
        builder.row(types.InlineKeyboardButton(text="Отчет ходока", callback_data="settings.onHodokForm", icon_custom_emoji_id='5219885475241691837'))
        USE_FORM_HODOK = '❌ Выключено'
    else:
        builder.row(types.InlineKeyboardButton(text="Отчет ходока", callback_data="settings.offHodokForm", icon_custom_emoji_id='5219791114810199158', style='success'))
        USE_FORM_HODOK = '✅ Включено'
    if DATA_USER[18] == 0:
        builder.row(types.InlineKeyboardButton(text="Помощь старших", callback_data="settings.onHelp", icon_custom_emoji_id='5219885475241691837'))
        SETTINGS_HELP = '❌ Выключено'
    else:
        builder.row(types.InlineKeyboardButton(text="Помощь старших", callback_data="settings.offHelp", icon_custom_emoji_id='5219791114810199158', style='success'))
        SETTINGS_HELP = '✅ Включена'
    builder.row(types.InlineKeyboardButton(text="Изменить шаблон", callback_data="settings.profiles", icon_custom_emoji_id='5219952167493867867'))
    builder.row(types.InlineKeyboardButton(text="Настройка кнопок", callback_data="settings.buttons", icon_custom_emoji_id='5219899605684098553'))
    builder.row(types.InlineKeyboardButton(text="Выбрать смещение", callback_data="settings.smchange", icon_custom_emoji_id='5219741860125251546'))
    builder.row(types.InlineKeyboardButton(text="Очистка данных", callback_data="settings.clearMenu", icon_custom_emoji_id='5219899605684098553'))

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
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.Show", icon_custom_emoji_id='5220091062441251597'))
    builder.row(types.InlineKeyboardButton(text="Митя", callback_data="settings.setsm0", icon_custom_emoji_id='5219741860125251546'))
    builder.add(types.InlineKeyboardButton(text="Степа", callback_data="settings.setsm1", icon_custom_emoji_id='5219741860125251546'))
    builder.add(types.InlineKeyboardButton(text="Олег", callback_data="settings.setsm2", icon_custom_emoji_id='5219741860125251546'))
    builder.add(types.InlineKeyboardButton(text="Артем", callback_data="settings.setsm3", icon_custom_emoji_id='5219741860125251546'))

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
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.Show", icon_custom_emoji_id='5220091062441251597'))
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
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.Show", icon_custom_emoji_id='5220091062441251597'))
    builder.row(types.InlineKeyboardButton(text="➕ Добавить свою кнопку", callback_data="settings.buttonsAdd"))
    builder.row(types.InlineKeyboardButton(text="➕ Добавить свою категорию", callback_data="settings.buttonsAddCategory"))
    builder.row(types.InlineKeyboardButton(text="❌ Удалить кнопку", callback_data="settings.buttonsDelete"))
    builder.row(types.InlineKeyboardButton(text="📝 Редактировать кнопки", callback_data="settings.buttonsEdit"))

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



@router.callback_query(F.data == 'settings.buttonsAddCategory')
async def buttonsAddCategory(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttonsAddCategoryCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)
    await database.setUserID(message.from_user.id, 'temporary', "'[]'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 📱 » ➕ Добавить свою категории\n\n"
             f"📝 Введите название кнопки",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'settings.buttonsAddCategoryCheck')
async def buttonsAddCategoryCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttonsAddCategoryCheck2'")
    DATA_USER = await database.getUserID(message.from_user.id)

    TEMPORARY = []
    TEMPORARY.append(message.text)
    await database.setUserID(message.from_user.id, 'temporary', f'\"{TEMPORARY}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 📱 » ➕ Добавить свою категорию\n\n"
             f"📝 Укажите массив кнопок для категории (можно и подкатегории)\n"
             f"Пример: [['BASEACTION1', 'BASEACTION2'], ['BASEACTION3']]",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'settings.buttonsAddCategoryCheck2')
async def buttonsAddCategoryCheck2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttons'")
    DATA_USER = await database.getUserID(message.from_user.id)

    TEMPORARY = ast.literal_eval(DATA_USER[14])
    TEMPORARY.append(message.text)
    NAME_GATE = f'USERCATEGORY-{random.randint(1, 999999999)}'
    await database.addNewData('actions', 'idGate, nameButton, textLogs, coast', f"'{NAME_GATE}', '{TEMPORARY[0]}', \"{TEMPORARY[1]}\", '0'")
    ID = await database.sqlRequest('SELECT * FROM actions ORDER BY id DESC LIMIT 1;')
    USER_ACTIONS = ast.literal_eval(DATA_USER[5])
    USER_ACTIONS.append([f"{NAME_GATE}"])
    await database.setUserID(message.from_user.id, 'actions', f'\"{USER_ACTIONS}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ Кнопка добавлена",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())













@router.callback_query(F.data == 'settings.buttonsEdit')
async def buttonsEdit(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttonsEditCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 📱 » 📝 Редактировать кнопки\n\n"
             f"📝 Введите массив, который хотите установить",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'settings.buttonsEditCheck')
async def buttonsEditCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttonsEditCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))
    await database.setUserID(message.from_user.id, 'actions', f'\"{message.text}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ Массив кнопок установлен!",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'settings.buttonsAdd')
async def buttonsAdd(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttonsAddCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)
    await database.setUserID(message.from_user.id, 'temporary', "'[]'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 📱 » ➕ Добавить свою кнопку\n\n"
             f"📝 Введите название кнопки",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'settings.buttonsAddCheck')
async def buttonsAddCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttonsAddCheck2'")
    DATA_USER = await database.getUserID(message.from_user.id)

    TEMPORARY = []
    TEMPORARY.append(message.text)
    await database.setUserID(message.from_user.id, 'temporary', f'\"{TEMPORARY}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 📱 » ➕ Добавить свою кнопку\n\n"
             f"📝 Укажите текст для логов",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'settings.buttonsAddCheck2')
async def buttonsAddCheck2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttons'")
    DATA_USER = await database.getUserID(message.from_user.id)

    TEMPORARY = ast.literal_eval(DATA_USER[14])
    TEMPORARY.append(message.text)
    await database.setUserID(message.from_user.id, 'temporary', f'\"{TEMPORARY}\"')
    NAME_GATE = f'USERBUTTON-{random.randint(1, 999999999)}'
    await database.addNewData('actions', 'idGate, nameButton, textLogs, coast', f"'{NAME_GATE}', '{TEMPORARY[0]}', '{TEMPORARY[1]}', '0'")
    ID = await database.sqlRequest('SELECT * FROM actions ORDER BY id DESC LIMIT 1;')
    USER_ACTIONS = ast.literal_eval(DATA_USER[5])
    USER_ACTIONS.append([f"{NAME_GATE}"])
    await database.setUserID(message.from_user.id, 'actions', f'\"{USER_ACTIONS}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ Кнопка добавлена",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'settings.buttonsDelete')
async def buttonsDelete(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttonsDelete'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))
    BUTTONS = ast.literal_eval(DATA_USER[5])
    for button in BUTTONS:
        count = 0
        for subbutton in button:
            button_data = await database.getData('actions', 'idGate', f"'{subbutton}'")
            if count == 0:
                builder.row(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"settings.buttonsDeleteACTION-{button_data[1]}"))
            else:
                builder.add(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"settings.buttonsDeleteACTION-{button_data[1]}"))
            count = count + 1

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 📱 » ❌ Удалить кнопку\n\n"
             f"Выберите кнопку, которую желаете удалить из клавиатуры",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('settings.buttonsDeleteACTION-'))
async def buttonsDeleteACTION(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'settings.buttonsDeleteACTION'")
    DATA_USER = await database.getUserID(message.from_user.id)

    idGate = message.data.replace('settings.buttonsDeleteACTION-', '')
    DATA_ACTIONS = ast.literal_eval(DATA_USER[5])
    print(DATA_ACTIONS)
    print(idGate)
    for i, sublist in enumerate(DATA_ACTIONS):
        if idGate in sublist:
            sublist.remove(idGate)  # Удаляем элемент
            removed = True
            print(f"Элемент '{idGate}' успешно удалён")

            # Проверяем, стал ли подсписок пустым
            if len(sublist) == 0:
                DATA_ACTIONS.pop(i)  # Удаляем пустой подсписок по индексу
                print("Пустой подсписок удалён из структуры")

            break  # Прекращаем поиск после первого вхождения
    await database.setUserID(message.from_user.id, 'actions', f'\"{DATA_ACTIONS}\"')
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.buttons", icon_custom_emoji_id='5220091062441251597'))
    BUTTONS = ast.literal_eval(DATA_USER[5])
    for button in BUTTONS:
        count = 0
        for subbutton in button:
            button_data = await database.getData('actions', 'idGate', f"'{subbutton}'")
            if count == 0:
                builder.row(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"settings.buttonsDeleteACTION-{button_data[1]}"))
            else:
                builder.add(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"settings.buttonsDeleteACTION-{button_data[1]}"))
            count = count + 1

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 📱 » ❌ Удалить кнопку\n\n"
             f"✅ Кнопка удалена\n\n"
             f"Выберите кнопку, которую желаете удалить из клавиатуры",
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
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="settings.Show", icon_custom_emoji_id='5220091062441251597'))
    builder.row(types.InlineKeyboardButton(text="🔄 МЛП", callback_data="settings.profilesMLPChange"))
    builder.add(types.InlineKeyboardButton(text="🔄 Ходок", callback_data="settings.profilesHodokChange"))
    builder.row(types.InlineKeyboardButton(text="🤖 Пустая клавиатура МЛП", callback_data="settings.profilesMLPEmpty"))
    builder.row(types.InlineKeyboardButton(text="🤖 Использовать МЛП", callback_data="settings.profilesMLP"))
    builder.row(types.InlineKeyboardButton(text="🤖 Использовать МЛП (минимал)", callback_data="settings.profilesMLPMin"))
    builder.row(types.InlineKeyboardButton(text="🏃‍➡️ Пустая клавиатура ходока", callback_data="settings.profilesHodokEmpty"))
    builder.row(types.InlineKeyboardButton(text="🏃‍➡️ Использовать ходоковский", callback_data="settings.profilesHodok"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » ⚙️ » 🗂 Изменить шаблон\n\n"
             f"🗂 Шаблон » {DATA_USER[13]}\n\n"
             f"Шаблоны — это готовый пресет кнопок и функций для комфортной работы в выбранной задаче. В данный момент есть два готовых шаблона: МЛП и ходоковские",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())




@router.callback_query(F.data == 'settings.profilesMLPChange')
async def profilesMLPChange(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.profiles'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    await database.setUserID(message.from_user.id, 'profile', f"'МЛП'")
    await message.answer(
        text="✅ Установлен тип МЛП",
        show_alert=False
    )
    await profiles(message, bot)


@router.callback_query(F.data == 'settings.profilesHodokChange')
async def profilesHodokChange(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.profiles'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    await database.setUserID(message.from_user.id, 'profile', f"'Ходок'")
    await message.answer(
        text="✅ Установлен тип ходока",
        show_alert=False
    )
    await profiles(message, bot)



@router.callback_query(F.data == 'settings.profilesHodokEmpty')
async def profilesHodokEmpty(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.profiles'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ACTIONS = []
    await database.setUserID(message.from_user.id, 'actions', f'\"{ACTIONS}\"')
    await database.setUserID(message.from_user.id, 'profile', f"'Ходок'")
    await message.answer(
        text="✅ Установлен новый шаблон",
        show_alert=False
    )
    await profiles(message, bot)



@router.callback_query(F.data == 'settings.profilesMLPEmpty')
async def profilesMLPEmpty(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'settings.profiles'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ACTIONS = []
    await database.setUserID(message.from_user.id, 'actions', f'\"{ACTIONS}\"')
    await database.setUserID(message.from_user.id, 'profile', f"'МЛП'")
    await message.answer(
        text="✅ Установлен новый шаблон",
        show_alert=False
    )
    await profiles(message, bot)


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
    await clearMenu(message, bot)


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
    await clearMenu(message, bot)


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
    await clearMenu(message, bot)


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
    await clearMenu(message, bot)



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

    await database.setUserID(message.from_user.id, 'settings_help', "'1'")
    await message.answer(
        text="✅ Включено",
        show_alert=False
    )
    await Show(message, bot)



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