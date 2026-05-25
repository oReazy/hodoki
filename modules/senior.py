import asyncio, logging, time, states, ast

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types, html, F, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database
from modules.database import PASSWORD

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

router = Router()

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

@router.callback_query(F.data == 'senior.Show')
async def Show(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.Show'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="mainMenu.Show"))
    builder.row(types.InlineKeyboardButton(text="⚙️ Локации", callback_data="senior.Locations"))
    builder.add(types.InlineKeyboardButton(text="⚙️ Роботы", callback_data="senior.none"))
    builder.row(types.InlineKeyboardButton(text="⚙️ Сотрудники", callback_data="senior.none"))
    builder.add(types.InlineKeyboardButton(text="🗓 Расписание", callback_data="senior.none"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 Старший смены\n\n"
             f"В данный момент локаций: 0\n"
             f"Количество роботов: 0\n"
             f"Количество сотрудников: 0 (0; 0; 0; 0)",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'senior.Locations')
async def Locations(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.Locations'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    # DATA_LOCATIONS = await database.sqlRequest('SELECT * FROM `locations`')
    DATA_LOCATIONS = await database.getDataAllMulti('locations')
    TEXT = ''
    if len(DATA_LOCATIONS) > 0:
        TEXT = '\n\n'
        for item in DATA_LOCATIONS:
            if item[2] == 0:
                TEXT = f'{TEXT}<blockquote>{item[1]}, не работает, {item[3]}, {item[4]}</blockquote>\n'
            elif item[2] == 1:
                TEXT = f'{TEXT}<blockquote>{item[1]}, работает, {item[3]}, {item[4]}</blockquote>\n'

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Show"))
    builder.row(types.InlineKeyboardButton(text="🟢 Все", callback_data="senior.Locations"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Рабочие", callback_data="senior.LocationsStatus1"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Нерабочие", callback_data="senior.LocationsStatus0"))
    builder.row(types.InlineKeyboardButton(text="⚪️ МЛП", callback_data="senior.LocationsTypeМЛП"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Ходоки", callback_data="senior.LocationsTypeХодоки"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Спецзадание", callback_data="senior.LocationsTypeСпецзадание"))
    builder.row(types.InlineKeyboardButton(text="➕ Добавить локацию", callback_data="senior.LocationsAdd"))
    builder.row(types.InlineKeyboardButton(text="📝 Редактировать локацию", callback_data="senior.none"))
    builder.row(types.InlineKeyboardButton(text="❌ Удалить локацию", callback_data="senior.none"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ Локации"
             f"{TEXT}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'senior.LocationsStatus1')
async def LocationsStatus1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.LocationsStatus1'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    # DATA_LOCATIONS = await database.sqlRequest('SELECT * FROM `locations`')
    DATA_LOCATIONS = await database.getDataMulti('locations', 'lock_route', "'1'")
    TEXT = ''
    if len(DATA_LOCATIONS) > 0:
        TEXT = '\n\n'
        for item in DATA_LOCATIONS:
            TEXT = f'{TEXT}<blockquote>{item[1]}, работает, {item[3]}, {item[4]}</blockquote>\n'

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Show"))
    builder.row(types.InlineKeyboardButton(text="⚪️ Все", callback_data="senior.Locations"))
    builder.add(types.InlineKeyboardButton(text="🟢 Рабочие", callback_data="senior.LocationsStatus1"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Нерабочие", callback_data="senior.LocationsStatus0"))
    builder.row(types.InlineKeyboardButton(text="⚪️ МЛП", callback_data="senior.LocationsTypeМЛП"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Ходоки", callback_data="senior.LocationsTypeХодоки"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Спецзадание", callback_data="senior.LocationsTypeСпецзадание"))
    builder.row(types.InlineKeyboardButton(text="➕ Добавить локацию", callback_data="senior.LocationsAdd"))
    builder.row(types.InlineKeyboardButton(text="📝 Редактировать локацию", callback_data="senior.none"))
    builder.row(types.InlineKeyboardButton(text="❌ Удалить локацию", callback_data="senior.none"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ Локации"
             f"{TEXT}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'senior.LocationsStatus0')
async def LocationsStatus0(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.LocationsStatus0'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    # DATA_LOCATIONS = await database.sqlRequest('SELECT * FROM `locations`')
    DATA_LOCATIONS = await database.getDataMulti('locations', 'lock_route', "'0'")
    TEXT = ''
    if len(DATA_LOCATIONS) > 0:
        TEXT = '\n\n'
        for item in DATA_LOCATIONS:
            TEXT = f'{TEXT}<blockquote>{item[1]}, не работает, {item[3]}, {item[4]}</blockquote>\n'

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Show"))
    builder.row(types.InlineKeyboardButton(text="⚪️ Все", callback_data="senior.Locations"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Рабочие", callback_data="senior.LocationsStatus1"))
    builder.add(types.InlineKeyboardButton(text="🟢 Нерабочие", callback_data="senior.LocationsStatus0"))
    builder.row(types.InlineKeyboardButton(text="⚪️ МЛП", callback_data="senior.LocationsTypeМЛП"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Ходоки", callback_data="senior.LocationsTypeХодоки"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Спецзадание", callback_data="senior.LocationsTypeСпецзадание"))
    builder.row(types.InlineKeyboardButton(text="➕ Добавить локацию", callback_data="senior.LocationsAdd"))
    builder.row(types.InlineKeyboardButton(text="📝 Редактировать локацию", callback_data="senior.none"))
    builder.row(types.InlineKeyboardButton(text="❌ Удалить локацию", callback_data="senior.none"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ Локации"
             f"{TEXT}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('senior.LocationsType'))
async def LocationsType(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.LocationsType'")
    DATA_USER = await database.getUserID(message.from_user.id)
    idGate = message.data.replace('senior.LocationsType', '')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_LOCATIONS = await database.getDataMulti('locations', 'type', f"'{idGate}'")
    TEXT = ''
    if len(DATA_LOCATIONS) > 0:
        TEXT = '\n\n'
        for item in DATA_LOCATIONS:
            if item[2] == 0:
                TEXT = f'{TEXT}<blockquote>{item[1]}, не работает, {item[3]}, {item[4]}</blockquote>\n'
            elif item[2] == 1:
                TEXT = f'{TEXT}<blockquote>{item[1]}, работает, {item[3]}, {item[4]}</blockquote>\n'

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Show"))
    builder.row(types.InlineKeyboardButton(text="⚪️ Все", callback_data="senior.Locations"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Рабочие", callback_data="senior.LocationsStatus1"))
    builder.add(types.InlineKeyboardButton(text="⚪️ Нерабочие", callback_data="senior.LocationsStatus0"))
    if idGate == 'МЛП': builder.row(types.InlineKeyboardButton(text="🟢 МЛП", callback_data="senior.LocationsTypeМЛП"))
    else: builder.row(types.InlineKeyboardButton(text="⚪️ МЛП", callback_data="senior.LocationsTypeМЛП"))
    if idGate == 'Ходоки': builder.add(types.InlineKeyboardButton(text="🟢 Ходоки", callback_data="senior.LocationsTypeХодоки"))
    else: builder.add(types.InlineKeyboardButton(text="⚪️ Ходоки", callback_data="senior.LocationsTypeХодоки"))
    if idGate == 'Спецзадание': builder.add(types.InlineKeyboardButton(text="🟢 Спецзадание", callback_data="senior.LocationsTypeСпецзадание"))
    else: builder.add(types.InlineKeyboardButton(text="⚪️ Спецзадание", callback_data="senior.LocationsTypeСпецзадание"))
    builder.row(types.InlineKeyboardButton(text="➕ Добавить локацию", callback_data="senior.LocationsAdd"))
    builder.row(types.InlineKeyboardButton(text="📝 Редактировать локацию", callback_data="senior.none"))
    builder.row(types.InlineKeyboardButton(text="❌ Удалить локацию", callback_data="senior.none"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ Локации"
             f"{TEXT}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'senior.LocationsAdd')
async def LocationsAdd(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'senior.LocationsAddCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    temporary = []
    await database.setUserID(message.from_user.id, 'temporary', f'\"{temporary}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Locations"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ » ➕ Добавить локацию\n\n"
             f"📝 Введите название локации",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'senior.LocationsAddCheck')
async def LocationsAddCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.LocationsAddCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    TEMPORARY_INFO = ast.literal_eval(DATA_USER[14])
    TEMPORARY_INFO.append(message.text)
    await database.setUserID(message.from_user.id, 'temporary', f'\"{TEMPORARY_INFO}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await LocationsAddGeo(message, bot)



@router.callback_query(F.data == 'senior.LocationsAddGeo')
async def LocationsAddGeo(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'senior.LocationsAddGeoCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Locations"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ » ➕ Добавить локацию\n\n"
             f"📝 Введите координаты локации",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'senior.LocationsAddGeoCheck')
async def LocationsAddGeoCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.LocationsAddGeoCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    TEMPORARY_INFO = ast.literal_eval(DATA_USER[14])
    TEMPORARY_INFO.append(message.text)
    await database.setUserID(message.from_user.id, 'temporary', f'\"{TEMPORARY_INFO}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await LocationsAddStatus(message, bot)


@router.callback_query(F.data == 'senior.LocationsAddStatus')
async def LocationsAddStatus(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.LocationsAddStatus'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Locations"))
    builder.row(types.InlineKeyboardButton(text="Работает", callback_data="senior.LocationsAddStatus1"))
    builder.add(types.InlineKeyboardButton(text="Не работает", callback_data="senior.LocationsAddStatus0"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ » ➕ Добавить локацию\n\n"
             f"📝 Выберите статус локации",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'senior.LocationsAddStatus0')
async def LocationsAddStatus0(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.Locations'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    TEMPORARY_INFO = ast.literal_eval(DATA_USER[14])
    TEMPORARY_INFO.append(0)
    await database.setUserID(message.from_user.id, 'temporary', f'\"{TEMPORARY_INFO}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Locations"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ » ➕ Добавить локацию\n\n"
             f"✅ Локация добавлена, статус установлен «Не рабочая»",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'senior.LocationsAddStatus1')
async def LocationsAddStatus1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.Locations'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    TEMPORARY_INFO = ast.literal_eval(DATA_USER[14])
    TEMPORARY_INFO.append(1)
    await database.setUserID(message.from_user.id, 'temporary', f'\"{TEMPORARY_INFO}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await LocationsAddType(message, bot)


@router.callback_query(F.data == 'senior.LocationsAddType')
async def LocationsAddType(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.LocationsAddType'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Locations"))
    builder.row(types.InlineKeyboardButton(text="МЛП", callback_data="senior.LocationsAddTypeCheckМЛП"))
    builder.add(types.InlineKeyboardButton(text="Ходоки", callback_data="senior.LocationsAddTypeCheckХодоки"))
    builder.add(types.InlineKeyboardButton(text="Спецзадание", callback_data="senior.LocationsAddTypeCheckСпецзадание"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ » ➕ Добавить локацию\n\n"
             f"📝 Выберите тип локации (на чем базируется данная локация)",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data.startswith('senior.LocationsAddTypeCheck'))
async def LocationsAddTypeCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'senior.Locations'")
    DATA_USER = await database.getUserID(message.from_user.id)
    idGate = message.data.replace('senior.LocationsAddTypeCheck', '')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    TEMPORARY_INFO = ast.literal_eval(DATA_USER[14])
    await database.addNewData('locations', 'name, lock_route, geo, type', f"'{TEMPORARY_INFO[0]}', '{TEMPORARY_INFO[2]}', '{TEMPORARY_INFO[1]}', '{idGate}'")

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="senior.Locations"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🛠 » ⚙️ » ➕ Добавить локацию\n\n"
             f"✅ Локация добавлена, статус установлен «Рабочая»",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())

