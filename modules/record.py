import asyncio, logging, time, states, ast, datetime

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types, html, F, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database, mainMenu

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

router = Router()

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————


@router.callback_query(F.data == 'record.StartRobot')
async def StartRobot(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)
    await database.setUserID(message.from_user.id, 'logs', "'[]'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="❌ Отменить запись", callback_data="mainMenu.Show"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[10])
    if len(ROBOT_INFO[0]) == 1:
        builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[0][0]}", callback_data="record.StartRobotVAR1"))
    if len(ROBOT_INFO[0]) == 2:
        builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[0][0]}", callback_data="record.StartRobotVAR1"))
        builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[0][1]}", callback_data="record.StartRobotVAR2"))
    if len(ROBOT_INFO[0]) == 3:
        builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[0][0]}", callback_data="record.StartRobotVAR1"))
        builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[0][1]}", callback_data="record.StartRobotVAR2"))
        builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[0][2]}", callback_data="record.StartRobotVAR3"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🟩 Начать запись\n\n"
             f"📝 Введите номер робота на котором будете вести запись или выберите из последних используемых",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'record.StartRobotVAR1')
async def StartRobotVAR1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[0] = ROBOT_INFO_ARCHIVE[0][0]
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await StartRoute(message, bot)


@router.callback_query(F.data == 'record.StartRobotVAR2')
async def StartRobotVAR2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[0] = ROBOT_INFO_ARCHIVE[0][1]
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await StartRoute(message, bot)


@router.callback_query(F.data == 'record.StartRobotVAR3')
async def StartRobotVAR3(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[0] = ROBOT_INFO_ARCHIVE[0][2]
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await StartRoute(message, bot)




@router.callback_query(F.data == 'record.StartRobotCheck')
async def StartRobotCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    if message.text.isdigit():
        ROBOT_INFO = ast.literal_eval(DATA_USER[8])
        ROBOT_INFO[0] = int(message.text)
        ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
        if len(ROBOT_INFO_ARCHIVE[0]) == 3:
            ROBOT_INFO_ARCHIVE[0].pop
            ROBOT_INFO_ARCHIVE[0][2] = ROBOT_INFO_ARCHIVE[0][1]
            ROBOT_INFO_ARCHIVE[0][1] = ROBOT_INFO_ARCHIVE[0][0]
            ROBOT_INFO_ARCHIVE[0][0] = int(message.text)
        else:
            if len(ROBOT_INFO_ARCHIVE[0]) == 0:
                ROBOT_INFO_ARCHIVE[0].append(int(message.text))
            elif len(ROBOT_INFO_ARCHIVE[0]) == 1:
                ROBOT_INFO_ARCHIVE[0].append(ROBOT_INFO_ARCHIVE[0][0])
                ROBOT_INFO_ARCHIVE[0][0] = int(message.text)
            elif len(ROBOT_INFO_ARCHIVE[0]) == 2:
                ROBOT_INFO_ARCHIVE[0].append(ROBOT_INFO_ARCHIVE[0][1])
                ROBOT_INFO_ARCHIVE[0][1] = ROBOT_INFO_ARCHIVE[0][0]
                ROBOT_INFO_ARCHIVE[0][0] = int(message.text)
        await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
        await database.setUserID(message.from_user.id, 'robot_info_archive', f'\"{ROBOT_INFO_ARCHIVE}\"')
        await StartRoute(message, bot)
    else:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="❌ Отменить запись", callback_data="mainMenu.Show"))
        ROBOT_INFO = ast.literal_eval(DATA_USER[10])
        if len(ROBOT_INFO[0]) == 1:
            builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[0][0]}", callback_data="record.StartRobotVAR1"))
        if len(ROBOT_INFO[0]) == 2:
            builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[0][0]}", callback_data="record.StartRobotVAR1"))
            builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[0][1]}", callback_data="record.StartRobotVAR2"))
        if len(ROBOT_INFO[0]) == 3:
            builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[0][0]}", callback_data="record.StartRobotVAR1"))
            builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[0][1]}", callback_data="record.StartRobotVAR2"))
            builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[0][2]}", callback_data="record.StartRobotVAR3"))

        # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        MAIN = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"🎯 » 🟩 Начать запись\n\n"
                 f"❌ Укажите робота цифрами\n\n"
                 f"📝 Введите номер робота на котором будете вести запись или выберите из последних используемых",
            message_id=DATA_USER[2],
            reply_markup=builder.as_markup())





@router.callback_query(F.data == 'record.StartRoute')
async def StartRoute(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRouteCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="❌ Отменить запись", callback_data="mainMenu.Show"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[10])
    if len(ROBOT_INFO[1]) == 1:
        builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[1][0]}", callback_data="record.StartRouteVAR1"))
    if len(ROBOT_INFO[1]) == 2:
        builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[1][0]}", callback_data="record.StartRouteVAR1"))
        builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[1][1]}", callback_data="record.StartRouteVAR2"))
    if len(ROBOT_INFO[1]) == 3:
        builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[1][0]}", callback_data="record.StartRouteVAR1"))
        builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[1][1]}", callback_data="record.StartRouteVAR2"))
        builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[1][2]}", callback_data="record.StartRouteVAR3"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🟩 Начать запись\n\n"
             f"📝 Введите номер маршрута или выберите из последних",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'record.StartRouteVAR1')
async def StartRouteVAR1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[1] = ROBOT_INFO_ARCHIVE[1][0]
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await recordLogs(message, bot)


@router.callback_query(F.data == 'record.StartRouteVAR2')
async def StartRouteVAR2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[1] = ROBOT_INFO_ARCHIVE[1][1]
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await recordLogs(message, bot)


@router.callback_query(F.data == 'record.StartRouteVAR3')
async def StartRouteVAR3(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[1] = ROBOT_INFO_ARCHIVE[1][2]
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await recordLogs(message, bot)




@router.callback_query(F.data == 'record.StartRouteCheck')
async def StartRouteCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRouteCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    if message.text.isdigit():
        ROBOT_INFO = ast.literal_eval(DATA_USER[8])
        ROBOT_INFO[1] = int(message.text)
        ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
        if len(ROBOT_INFO_ARCHIVE[1]) == 3:
            ROBOT_INFO_ARCHIVE[1].pop
            ROBOT_INFO_ARCHIVE[1][2] = ROBOT_INFO_ARCHIVE[1][1]
            ROBOT_INFO_ARCHIVE[1][1] = ROBOT_INFO_ARCHIVE[1][0]
            ROBOT_INFO_ARCHIVE[1][0] = int(message.text)
        else:
            if len(ROBOT_INFO_ARCHIVE[1]) == 0:
                ROBOT_INFO_ARCHIVE[1].append(int(message.text))
            elif len(ROBOT_INFO_ARCHIVE[1]) == 1:
                ROBOT_INFO_ARCHIVE[1].append(ROBOT_INFO_ARCHIVE[1][0])
                ROBOT_INFO_ARCHIVE[1][0] = int(message.text)
            elif len(ROBOT_INFO_ARCHIVE[1]) == 2:
                ROBOT_INFO_ARCHIVE[1].append(ROBOT_INFO_ARCHIVE[1][1])
                ROBOT_INFO_ARCHIVE[1][1] = ROBOT_INFO_ARCHIVE[1][0]
                ROBOT_INFO_ARCHIVE[1][0] = int(message.text)
        await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
        await database.setUserID(message.from_user.id, 'robot_info_archive', f'\"{ROBOT_INFO_ARCHIVE}\"')
        await recordLogs(message, bot)
    else:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="❌ Отменить запись", callback_data="mainMenu.Show"))
        ROBOT_INFO = ast.literal_eval(DATA_USER[10])
        if len(ROBOT_INFO[1]) == 1:
            builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[1][0]}", callback_data="record.StartRouteVAR1"))
        if len(ROBOT_INFO[1]) == 2:
            builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[1][0]}", callback_data="record.StartRouteVAR1"))
            builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[1][1]}", callback_data="record.StartRouteVAR2"))
        if len(ROBOT_INFO[1]) == 3:
            builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[1][0]}", callback_data="record.StartRouteVAR1"))
            builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[1][1]}", callback_data="record.StartRouteVAR2"))
            builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[1][2]}", callback_data="record.StartRouteVAR3"))

        # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        MAIN = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"🎯 » 🟩 Начать запись\n\n"
                 f"❌ Укажите робота цифрами\n\n"
                 f"📝 Введите номер маршрута или выберите из последних",
            message_id=DATA_USER[2],
            reply_markup=builder.as_markup())



@router.callback_query(F.data == 'record.recordLogs')
async def recordLogs(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.recordLogsText'")
    DATA_USER = await database.getUserID(message.from_user.id)
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    BUTTONS = ast.literal_eval(DATA_USER[5])
    LOGS = ast.literal_eval(DATA_USER[6])

    TEXT_LOGS = ''
    for item in LOGS:
        TEXT_LOGS = f"{TEXT_LOGS}\n{item}"

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stop"))
    builder.add(types.InlineKeyboardButton(text="❌ Удалить строку", callback_data="record.deleteStroke"))
    for button in BUTTONS:
        # [['BASEACTION1'], ['BASEACTION2', 'BASEACTION3'], ['BASEACTION4', 'BASEACTION5'], ['BASEACTION6'], ['BASEACTION7'], ['BASEACTION8'], ['BASEACTION9'], ['BASEACTION10'], ['BASEACTION11']]
        count = 0
        for subbutton in button:
            button_data = await database.getData('actions', 'idGate', f"'{subbutton}'")
            if count == 0:
                builder.row(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"record.usedButton-{button_data[1]}"))
            else:
                builder.add(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"record.usedButton-{button_data[1]}"))
            count = count + 1


    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🤖 <b>А{ROBOT_INFO[0]}</b> • 🗺 <b>Маршрут {ROBOT_INFO[1]}</b>\n"
             f"{TEXT_LOGS}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data.startswith('record.usedButton-'))
async def recordLogsButton(callback: types.CallbackQuery, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(callback.from_user.id, "tg_answer", "'1'")
    await database.setUserID(callback.from_user.id, "state", "'record.recordLogsText'")
    DATA_USER = await database.getUserID(callback.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    idGate = callback.data.replace('record.usedButton-', '')
    TEXT_FOR_LOGS = await database.getData('actions', 'idGate', f"'{idGate}'")
    now = datetime.datetime.now()
    if DATA_USER[9] == 0:
        current_time = now.strftime("%H:%M")
    else:
        current_time = now.strftime("%H:%M:%S")
    TEXT_FOR_LOGS = f'{current_time} {TEXT_FOR_LOGS[3]}'

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    BUTTONS = ast.literal_eval(DATA_USER[5])
    LOGS = ast.literal_eval(DATA_USER[6])
    LOGS.append(TEXT_FOR_LOGS)
    await database.setUserID(callback.from_user.id, 'logs', f'\"{LOGS}\"')
    DATA_USER = await database.getUserID(callback.from_user.id)
    LOGS = ast.literal_eval(DATA_USER[6])

    TEXT_LOGS = ''
    for item in LOGS:
        TEXT_LOGS = f"{TEXT_LOGS}\n{item}"

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stop"))
    builder.add(types.InlineKeyboardButton(text="❌ Удалить строку", callback_data="record.deleteStroke"))
    for button in BUTTONS:
        # [['BASEACTION1'], ['BASEACTION2', 'BASEACTION3'], ['BASEACTION4', 'BASEACTION5'], ['BASEACTION6'], ['BASEACTION7'], ['BASEACTION8'], ['BASEACTION9'], ['BASEACTION10'], ['BASEACTION11'], ['BASEACTION12', 'BASEACTION13', 'BASEACTION14'], ['BASEACTION15']]
        count = 0
        for subbutton in button:
            button_data = await database.getData('actions', 'idGate', f"'{subbutton}'")
            if count == 0:
                builder.row(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"record.usedButton-{button_data[1]}"))
            else:
                builder.add(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"record.usedButton-{button_data[1]}"))
            count = count + 1


    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=callback.from_user.id,
        text=f"🤖 <b>А{ROBOT_INFO[0]}</b> • 🗺 <b>Маршрут {ROBOT_INFO[1]}</b>\n"
             f"{TEXT_LOGS}",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'record.recordLogsText')
async def recordLogsText(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.recordLogsText'")
    DATA_USER = await database.getUserID(message.from_user.id)
    now = datetime.datetime.now()
    if DATA_USER[9] == 0:
        current_time = now.strftime("%H:%M")
    else:
        current_time = now.strftime("%H:%M:%S")
    TEXT_FOR_LOGS = f'{current_time} {message.text}'

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    BUTTONS = ast.literal_eval(DATA_USER[5])
    LOGS = ast.literal_eval(DATA_USER[6])
    LOGS.append(TEXT_FOR_LOGS)
    await database.setUserID(message.from_user.id, 'logs', f'\"{LOGS}\"')
    DATA_USER = await database.getUserID(message.from_user.id)
    LOGS = ast.literal_eval(DATA_USER[6])

    TEXT_LOGS = ''
    for item in LOGS:
        TEXT_LOGS = f"{TEXT_LOGS}\n{item}"

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stop"))
    builder.add(types.InlineKeyboardButton(text="❌ Удалить строку", callback_data="record.deleteStroke"))
    for button in BUTTONS:
        # [['BASEACTION1'], ['BASEACTION2', 'BASEACTION3'], ['BASEACTION4', 'BASEACTION5'], ['BASEACTION6'], ['BASEACTION7'], ['BASEACTION8'], ['BASEACTION9'], ['BASEACTION10'], ['BASEACTION11']]
        count = 0
        for subbutton in button:
            button_data = await database.getData('actions', 'idGate', f"'{subbutton}'")
            if count == 0:
                builder.row(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"record.usedButton-{button_data[1]}"))
            else:
                builder.add(types.InlineKeyboardButton(text=f"{button_data[2]}", callback_data=f"record.usedButton-{button_data[1]}"))
            count = count + 1

        # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        MAIN = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"🤖 <b>А{ROBOT_INFO[0]}</b> • 🗺 <b>Маршрут {ROBOT_INFO[1]}</b>\n"
                 f"{TEXT_LOGS}",
            message_id=DATA_USER[2],
            reply_markup=builder.as_markup())





@router.callback_query(F.data == 'record.stop')
async def stop(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.stop'")
    DATA_USER = await database.getUserID(message.from_user.id)
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    LOGS_ARCHIVE = ast.literal_eval(DATA_USER[7])
    LOGS = ast.literal_eval(DATA_USER[6])
    LOGS.append([ROBOT_INFO[0], ROBOT_INFO[1]])

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    print(LOGS_ARCHIVE)
    if len(LOGS_ARCHIVE) == 3:
        LOGS_ARCHIVE.pop
        LOGS_ARCHIVE[2] = LOGS_ARCHIVE[1]
        LOGS_ARCHIVE[1] = LOGS_ARCHIVE[0]
        LOGS_ARCHIVE[0] = LOGS
    else:
        if len(LOGS_ARCHIVE) == 0:
            LOGS_ARCHIVE.append(LOGS)
        elif len(LOGS_ARCHIVE) == 1:
            LOGS_ARCHIVE.append(LOGS_ARCHIVE[0])
            LOGS_ARCHIVE[0] = LOGS
        elif len(LOGS_ARCHIVE) == 2:
            LOGS_ARCHIVE.append(LOGS_ARCHIVE[1])
            LOGS_ARCHIVE[1] = LOGS_ARCHIVE[0]
            LOGS_ARCHIVE[0] = LOGS
    print(LOGS_ARCHIVE)
    await database.setUserID(message.from_user.id, 'logs_archive', f'\"{LOGS_ARCHIVE}\"')
    await mainMenu.Show(message, bot)


@router.callback_query(F.data == 'record.deleteStroke')
async def deleteStroke(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.deleteStroke'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    LOGS_OLD = ast.literal_eval(DATA_USER[6])
    print(LOGS_OLD)
    LOGS_OLD.pop()
    print(LOGS_OLD)


    await database.setUserID(message.from_user.id, 'logs', f'\"{LOGS_OLD}\"')
    await message.answer(
        text="✅ Удалена последняя строка",
        show_alert=False
    )
    await recordLogs(message, bot)