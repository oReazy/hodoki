import asyncio, logging, time, states, ast, datetime, re, datetime

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
    if DATA_USER[13] != 'Ходок':
        await StartRoute(message, bot)
    else:
        await StartLocation(message, bot)


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
    if DATA_USER[13] != 'Ходок':
        await StartRoute(message, bot)
    else:
        await StartLocation(message, bot)


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
    if DATA_USER[13] != 'Ходок':
        await StartRoute(message, bot)
    else:
        await StartLocation(message, bot)




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
        if DATA_USER[13] != 'Ходок':
            await StartRoute(message, bot)
        else:
            await StartLocation(message, bot)
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











@router.callback_query(F.data == 'record.StartLocation')
async def StartLocation(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.StartLocationCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="❌ Отменить запись", callback_data="mainMenu.Show"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[10])
    if len(ROBOT_INFO[2]) == 1:
        builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[2][0]}", callback_data="record.StartLocationVAR1"))
    if len(ROBOT_INFO[2]) == 2:
        builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[2][0]}", callback_data="record.StartLocationVAR1"))
        builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[2][1]}", callback_data="record.StartLocationVAR2"))
    if len(ROBOT_INFO[2]) == 3:
        builder.row(types.InlineKeyboardButton(text=f"⚡️ {ROBOT_INFO[2][0]}", callback_data="record.StartLocationVAR1"))
        builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[2][1]}", callback_data="record.StartLocationVAR2"))
        builder.add(types.InlineKeyboardButton(text=f"{ROBOT_INFO[2][2]}", callback_data="record.StartLocationVAR3"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🟩 Начать запись\n\n"
             f"📝 Введите название локации или выберите из последних",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'record.StartLocationVAR1')
async def StartLocationVAR1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartLocationСheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[1] = ROBOT_INFO_ARCHIVE[2][0]
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await recordLogs(message, bot)


@router.callback_query(F.data == 'record.StartLocationVAR2')
async def StartLocationVAR2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartLocationСheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[1] = ROBOT_INFO_ARCHIVE[2][1]
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await recordLogs(message, bot)


@router.callback_query(F.data == 'record.StartLocationVAR3')
async def StartLocationVAR3(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartLocationСheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[1] = ROBOT_INFO_ARCHIVE[2][2]
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await recordLogs(message, bot)


@router.callback_query(F.data == 'record.StartLocationCheck')
async def StartLocationCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartLocationCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    ROBOT_INFO[1] = message.text
    ROBOT_INFO_ARCHIVE = ast.literal_eval(DATA_USER[10])
    if len(ROBOT_INFO_ARCHIVE[2]) == 3:
        ROBOT_INFO_ARCHIVE[2].pop
        ROBOT_INFO_ARCHIVE[2][2] = ROBOT_INFO_ARCHIVE[2][1]
        ROBOT_INFO_ARCHIVE[2][1] = ROBOT_INFO_ARCHIVE[2][0]
        ROBOT_INFO_ARCHIVE[2][0] = message.text
    else:
        if len(ROBOT_INFO_ARCHIVE[2]) == 0:
            ROBOT_INFO_ARCHIVE[2].append(message.text)
        elif len(ROBOT_INFO_ARCHIVE[2]) == 1:
            ROBOT_INFO_ARCHIVE[2].append(ROBOT_INFO_ARCHIVE[2][0])
            ROBOT_INFO_ARCHIVE[2][0] = message.text
        elif len(ROBOT_INFO_ARCHIVE[2]) == 2:
            ROBOT_INFO_ARCHIVE[2].append(ROBOT_INFO_ARCHIVE[2][1])
            ROBOT_INFO_ARCHIVE[2][1] = ROBOT_INFO_ARCHIVE[2][0]
            ROBOT_INFO_ARCHIVE[2][0] = message.text
    await database.setUserID(message.from_user.id, 'robot_info', f'\"{ROBOT_INFO}\"')
    await database.setUserID(message.from_user.id, 'robot_info_archive', f'\"{ROBOT_INFO_ARCHIVE}\"')
    await recordLogs(message, bot)








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
    if DATA_USER[15] == 0:
        builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stop"))
    else:
        if DATA_USER[13] != 'Ходок':
            builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stop"))
        else:
            builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stopBattery"))
    builder.add(types.InlineKeyboardButton(text="❌ Удалить строку", callback_data="record.deleteStroke"))
    if  DATA_USER[18] == 1:
        builder.row(types.InlineKeyboardButton(text="🛟 Помощь", callback_data="record.help"))
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
    TEXT_UP = ''
    if DATA_USER[13] != 'Ходок':
        TEXT_UP = f"🤖 <b>А{ROBOT_INFO[0]}</b> • 🗺 <b>Маршрут {ROBOT_INFO[1]}</b>\n"
    else:
        TEXT_UP = f"🤖 <b>А{ROBOT_INFO[0]}</b> • 🗺 <b>Локация {ROBOT_INFO[1]}</b>\n"

    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"{TEXT_UP}"
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
    if idGate == 'BASEACTION3':
        if DATA_USER[13] == 'Ходок':
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[0][0] = ERRORS[0][0] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][0] = ERRORS[1][0]  + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
    if idGate == 'BASEACTION1':
        if DATA_USER[13] == 'Ходок':
            pass
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][6] = ERRORS[1][6] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
    if idGate == 'BASEACTION4':
        if DATA_USER[13] == 'Ходок':
            pass
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][5] = ERRORS[1][5] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
    if idGate == 'BASEACTION5':
        if DATA_USER[13] == 'Ходок':
            pass
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][5] = ERRORS[1][5] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
    if idGate == 'BASEACTION6':
        if DATA_USER[13] == 'Ходок':
            pass
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][7] = ERRORS[1][7] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
    if idGate == 'BASEACTION11':
        if DATA_USER[13] == 'Ходок':
            pass
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][4] = ERRORS[1][4] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
    if idGate == 'BASEACTION15':
        if DATA_USER[13] == 'Ходок':
            pass
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][8] = ERRORS[1][8] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
    if idGate == 'BASEACTION16':
        if DATA_USER[13] == 'Ходок':
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[0][2] = ERRORS[0][2] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][2] = ERRORS[1][2] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
    if idGate == 'BASEACTION17':
        if DATA_USER[13] == 'Ходок':
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[0][1] = ERRORS[0][1] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][1] = ERRORS[1][1] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
    if idGate == 'BASEACTION18':
        if DATA_USER[13] == 'Ходок':
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[0][3] = ERRORS[0][3] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')
        else:
            ERRORS = ast.literal_eval(DATA_SERVER[6])
            ERRORS[1][3] = ERRORS[1][3] + 1
            await database.setData('settings', 'id', "'1'", 'errors', f'\"{ERRORS}\"')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    BUTTONS = ast.literal_eval(DATA_USER[5])
    LOGS = ast.literal_eval(DATA_USER[6])

    # ---
    parsed_data = []
    LOGS.append(TEXT_FOR_LOGS)
    for line in LOGS:
        # Ищем время в начале строки (HH:MM или HH:MM:SS)
        match = re.match(r'^(\d{1,2}):(\d{1,2})(?::(\d{2}))?', line)
        if not match:
            print(f"Ошибка: не удалось распознать время в строке: {line}")
            continue
        hour, minute, second = match.groups()
        second = second or '00'  # Если секунды отсутствуют, считаем их 00

        # Формируем строку времени для преобразования
        time_str = f"{hour}:{minute}:{second}"

        try:
            # Преобразуем в datetime (предполагаем текущую дату)
            dt = datetime.datetime.strptime(time_str, "%H:%M:%S")
            # Получаем timestamp (относительно начала дня)
            timestamp = dt.hour * 3600 + dt.minute * 60 + dt.second
            parsed_data.append((timestamp, line))
        except ValueError as e:
            print(f"Ошибка преобразования времени в строке '{line}': {e}")
    sorted_data = sorted(parsed_data, key=lambda x: x[0])
    result = [item[1] for item in sorted_data]
    LOGS = result
    await database.setUserID(callback.from_user.id, 'logs', f'\"{LOGS}\"')
    # ---
    DATA_USER = await database.getUserID(callback.from_user.id)
    LOGS = ast.literal_eval(DATA_USER[6])

    TEXT_LOGS = ''
    for item in LOGS:
        TEXT_LOGS = f"{TEXT_LOGS}\n{item}"

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    if DATA_USER[15] == 0:
        builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stop"))
    else:
        if DATA_USER[13] != 'Ходок':
            builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stop"))
        else:
            builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stopBattery"))
    builder.add(types.InlineKeyboardButton(text="❌ Удалить строку", callback_data="record.deleteStroke"))
    if  DATA_USER[18] == 1:
        builder.row(types.InlineKeyboardButton(text="🛟 Помощь", callback_data="record.help"))
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
    TEXT_UP = ''
    if DATA_USER[13] != 'Ходок':
        TEXT_UP = f"🤖 <b>А{ROBOT_INFO[0]}</b> • 🗺 <b>Маршрут {ROBOT_INFO[1]}</b>\n"
    else:
        TEXT_UP = f"🤖 <b>А{ROBOT_INFO[0]}</b> • 🗺 <b>Локация {ROBOT_INFO[1]}</b>\n"

    MAIN = await bot.edit_message_text(
        chat_id=callback.from_user.id,
        text=f"{TEXT_UP}"
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
    SUPER_SORT = 0
    if re.match(r'^\d{1,2}:\d{2}', message.text):
        TEXT_FOR_LOGS = f'{message.text}'
        SUPER_SORT = 1
    else:
        if DATA_USER[9] == 0:
            current_time = now.strftime("%H:%M")
            TEXT_FOR_LOGS = f'{current_time} {message.text}'
            SUPER_SORT = 0
        else:
            current_time = now.strftime("%H:%M:%S")
            TEXT_FOR_LOGS = f'{current_time} {message.text}'
            SUPER_SORT = 0

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    BUTTONS = ast.literal_eval(DATA_USER[5])
    LOGS = ast.literal_eval(DATA_USER[6])
    parsed_data = []
    if message.text == '/new_message' or message.text == '/start':
        pass
    else:
        if SUPER_SORT == 1:
            parts = message.text.split(' ', 1)  # Разбиваем по первому пробелу
            time_part = parts[0]  # "9:41"
            text_part = parts[1] if len(parts) > 1 else ""  # "Привет"

            # Форматируем время
            hours, minutes = map(int, time_part.split(':'))
            formatted_time = f"{hours:02d}:{minutes:02d}"

            TEXT_TO = ''
            if text_part:
                TEXT_TO = f"{formatted_time} {text_part}"
            else:
                TEXT_TO = formatted_time
            LOGS.append(TEXT_TO)
        else:
            LOGS.append(TEXT_FOR_LOGS)
        for line in LOGS:
            # Ищем время в начале строки (HH:MM или HH:MM:SS)
            match = re.match(r'^(\d{1,2}):(\d{1,2})(?::(\d{2}))?', line)
            if not match:
                print(f"Ошибка: не удалось распознать время в строке: {line}")
                continue
            hour, minute, second = match.groups()
            second = second or '00'  # Если секунды отсутствуют, считаем их 00

            # Формируем строку времени для преобразования
            time_str = f"{hour}:{minute}:{second}"

            try:
                # Преобразуем в datetime (предполагаем текущую дату)
                dt = datetime.datetime.strptime(time_str, "%H:%M:%S")
                # Получаем timestamp (относительно начала дня)
                timestamp = dt.hour * 3600 + dt.minute * 60 + dt.second
                parsed_data.append((timestamp, line))
            except ValueError as e:
                print(f"Ошибка преобразования времени в строке '{line}': {e}")
        sorted_data = sorted(parsed_data, key=lambda x: x[0])
        result = [item[1] for item in sorted_data]
        LOGS = result
        await database.setUserID(message.from_user.id, 'logs', f'\"{LOGS}\"')
    DATA_USER = await database.getUserID(message.from_user.id)
    LOGS = ast.literal_eval(DATA_USER[6])

    TEXT_LOGS = ''
    for item in LOGS:
        TEXT_LOGS = f"{TEXT_LOGS}\n{item}"

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    if DATA_USER[15] == 0:
        builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stop"))
    else:
        if DATA_USER[13] != 'Ходок':
            builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stop"))
        else:
            builder.row(types.InlineKeyboardButton(text="❌ Закончить запись", callback_data="record.stopBattery"))
    builder.add(types.InlineKeyboardButton(text="❌ Удалить строку", callback_data="record.deleteStroke"))
    if  DATA_USER[18] == 1:
        builder.row(types.InlineKeyboardButton(text="🛟 Помощь", callback_data="record.help"))
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
        TEXT_UP = ''
        if DATA_USER[13] != 'Ходок':
            TEXT_UP = f"🤖 <b>А{ROBOT_INFO[0]}</b> • 🗺 <b>Маршрут {ROBOT_INFO[1]}</b>\n"
        else:
            TEXT_UP = f"🤖 <b>А{ROBOT_INFO[0]}</b> • 🗺 <b>Локация {ROBOT_INFO[1]}</b>\n"

        MAIN = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"{TEXT_UP}"
                 f"{TEXT_LOGS}",
            message_id=DATA_USER[2],
            reply_markup=builder.as_markup())




@router.callback_query(F.data == 'record.stopBattery')
async def stopBattery(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.stopBatteryCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)
    LOGS = ast.literal_eval(DATA_USER[6])
    LOGS.append('')
    await database.setUserID(message.from_user.id, 'logs', f'\"{LOGS}\"')

    if DATA_USER[15] == 0:
        await stop(message, bot)
    else:

        # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="🪫 25%", callback_data="record.stopBattery1"))
        builder.add(types.InlineKeyboardButton(text="🔋 50%", callback_data="record.stopBattery2"))
        builder.add(types.InlineKeyboardButton(text="🔋 75%", callback_data="record.stopBattery3"))

        # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        MAIN = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"📝 Выберите из предложенных или напишите цифру заряда батареи",
            message_id=DATA_USER[2],
            reply_markup=builder.as_markup())



@router.callback_query(F.data == 'record.stopBatteryCheck')
async def stopBatteryCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    TEXT = message.text.replace('%', '')
    NEW_DATA = [f'{TEXT}%']
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stopSSD(message, bot)



@router.callback_query(F.data == 'record.stopBattery1')
async def stopBattery1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ['25%']
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stopSSD(message, bot)


@router.callback_query(F.data == 'record.stopBattery2')
async def stopBattery2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ['50%']
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stopSSD(message, bot)


@router.callback_query(F.data == 'record.stopBattery3')
async def stopBattery3(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ['75%']
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stopSSD(message, bot)


@router.callback_query(F.data == 'record.stopSSD')
async def stopSSD(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.stopSSDCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)
    LOGS = ast.literal_eval(DATA_USER[6])
    LOGS.append('\n\n')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💽 25%", callback_data="record.stopSSD1"))
    builder.add(types.InlineKeyboardButton(text="💽 50%", callback_data="record.stopSSD2"))
    builder.add(types.InlineKeyboardButton(text="💽 75%", callback_data="record.stopSSD3"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"📝 Выберите из предложенных или напишите цифру занятого объема памяти",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'record.stopSSDCheck')
async def stopSSDCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ast.literal_eval(DATA_USER[14])
    TEXT = message.text.replace('%', '')
    NEW_DATA.append(f'{TEXT}%')
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stopDistance(message, bot)


@router.callback_query(F.data == 'record.stopSSD1')
async def stopSSD1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ast.literal_eval(DATA_USER[14])
    NEW_DATA.append('25%')
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stopDistance(message, bot)


@router.callback_query(F.data == 'record.stopSSD2')
async def stopSSD2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ast.literal_eval(DATA_USER[14])
    NEW_DATA.append('50%')
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stopDistance(message, bot)


@router.callback_query(F.data == 'record.stopSSD3')
async def stopSSD3(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ast.literal_eval(DATA_USER[14])
    NEW_DATA.append('75%')
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stopDistance(message, bot)


@router.callback_query(F.data == 'record.stopDistance')
async def stopDistance(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.stopDistanceCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)
    LOGS = ast.literal_eval(DATA_USER[6])
    LOGS.append('\n\n')

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🚶🏻‍➡️ 10км", callback_data="record.stopDistance1"))
    builder.add(types.InlineKeyboardButton(text="🏃🏻‍➡️ 15км", callback_data="record.stopDistance2"))
    builder.add(types.InlineKeyboardButton(text="🚴🏻 20км", callback_data="record.stopDistance3"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"📝 Выберите из предложенных или напишите цифру пройденного километража",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'record.stopDistanceCheck')
async def stopDistanceCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ast.literal_eval(DATA_USER[14])
    TEXT = message.text.replace('км', '')
    TEXT = TEXT.replace('км.', '')
    NEW_DATA.append(f'{TEXT}км')
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stop(message, bot)



@router.callback_query(F.data == 'record.stopDistance1')
async def stopDistance1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ast.literal_eval(DATA_USER[14])
    NEW_DATA.append('10км')
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stop(message, bot)


@router.callback_query(F.data == 'record.stopDistance2')
async def stopDistance2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ast.literal_eval(DATA_USER[14])
    NEW_DATA.append('15км')
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stop(message, bot)


@router.callback_query(F.data == 'record.stopDistance3')
async def stopDistance3(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.StartRobotCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    NEW_DATA = ast.literal_eval(DATA_USER[14])
    NEW_DATA.append('20км')
    await database.setUserID(message.from_user.id, 'temporary', f'\"{NEW_DATA}\"')
    await stop(message, bot)















@router.callback_query(F.data == 'record.stop')
async def stop(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'record.stop'")
    DATA_USER = await database.getUserID(message.from_user.id)
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    if DATA_USER[13] == 'Ходок' and DATA_USER[15] == 1:
        TEMPORARY = ast.literal_eval(DATA_USER[14])
    LOGS_ARCHIVE = ast.literal_eval(DATA_USER[7])
    LOGS = ast.literal_eval(DATA_USER[6])
    if DATA_USER[13] == 'Ходок' and DATA_USER[15] == 1:
        LOGS.append(f"<blockquote>Батарея: {TEMPORARY[0]}")
        LOGS.append(f"Память: {TEMPORARY[1]}")
        LOGS.append(f"Накат: {TEMPORARY[2]}</blockquote>")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    TIME = int(time.time())
    if DATA_USER[13] != 'Ходок':
        LOGS.append([ROBOT_INFO[0], f'Маршрут {ROBOT_INFO[1]}', current_time])
    else:
        LOGS.append([ROBOT_INFO[0], f'Локация {ROBOT_INFO[1]}', current_time])
    await database.addNewData('logs', 'tg_id, time, logs', f"'{message.from_user.id}', {TIME}, \"{LOGS}\"")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    print(LOGS_ARCHIVE)
    if len(LOGS_ARCHIVE) == 10:
        LOGS_ARCHIVE.pop
        LOGS_ARCHIVE[9] = LOGS_ARCHIVE[8]
        LOGS_ARCHIVE[8] = LOGS_ARCHIVE[7]
        LOGS_ARCHIVE[7] = LOGS_ARCHIVE[6]
        LOGS_ARCHIVE[6] = LOGS_ARCHIVE[5]
        LOGS_ARCHIVE[5] = LOGS_ARCHIVE[4]
        LOGS_ARCHIVE[4] = LOGS_ARCHIVE[3]
        LOGS_ARCHIVE[3] = LOGS_ARCHIVE[2]
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
        elif len(LOGS_ARCHIVE) == 3:
            LOGS_ARCHIVE.append(LOGS_ARCHIVE[2])
            LOGS_ARCHIVE[2] = LOGS_ARCHIVE[1]
            LOGS_ARCHIVE[1] = LOGS_ARCHIVE[0]
            LOGS_ARCHIVE[0] = LOGS
        elif len(LOGS_ARCHIVE) == 4:
            LOGS_ARCHIVE.append(LOGS_ARCHIVE[3])
            LOGS_ARCHIVE[3] = LOGS_ARCHIVE[2]
            LOGS_ARCHIVE[2] = LOGS_ARCHIVE[1]
            LOGS_ARCHIVE[1] = LOGS_ARCHIVE[0]
            LOGS_ARCHIVE[0] = LOGS
        elif len(LOGS_ARCHIVE) == 5:
            LOGS_ARCHIVE.append(LOGS_ARCHIVE[4])
            LOGS_ARCHIVE[4] = LOGS_ARCHIVE[3]
            LOGS_ARCHIVE[3] = LOGS_ARCHIVE[2]
            LOGS_ARCHIVE[2] = LOGS_ARCHIVE[1]
            LOGS_ARCHIVE[1] = LOGS_ARCHIVE[0]
            LOGS_ARCHIVE[0] = LOGS
        elif len(LOGS_ARCHIVE) == 6:
            LOGS_ARCHIVE.append(LOGS_ARCHIVE[5])
            LOGS_ARCHIVE[5] = LOGS_ARCHIVE[4]
            LOGS_ARCHIVE[4] = LOGS_ARCHIVE[3]
            LOGS_ARCHIVE[3] = LOGS_ARCHIVE[2]
            LOGS_ARCHIVE[2] = LOGS_ARCHIVE[1]
            LOGS_ARCHIVE[1] = LOGS_ARCHIVE[0]
            LOGS_ARCHIVE[0] = LOGS
        elif len(LOGS_ARCHIVE) == 7:
            LOGS_ARCHIVE.append(LOGS_ARCHIVE[6])
            LOGS_ARCHIVE[6] = LOGS_ARCHIVE[5]
            LOGS_ARCHIVE[5] = LOGS_ARCHIVE[4]
            LOGS_ARCHIVE[4] = LOGS_ARCHIVE[3]
            LOGS_ARCHIVE[3] = LOGS_ARCHIVE[2]
            LOGS_ARCHIVE[2] = LOGS_ARCHIVE[1]
            LOGS_ARCHIVE[1] = LOGS_ARCHIVE[0]
            LOGS_ARCHIVE[0] = LOGS
        elif len(LOGS_ARCHIVE) == 8:
            LOGS_ARCHIVE.append(LOGS_ARCHIVE[7])
            LOGS_ARCHIVE[7] = LOGS_ARCHIVE[6]
            LOGS_ARCHIVE[6] = LOGS_ARCHIVE[5]
            LOGS_ARCHIVE[5] = LOGS_ARCHIVE[4]
            LOGS_ARCHIVE[4] = LOGS_ARCHIVE[3]
            LOGS_ARCHIVE[3] = LOGS_ARCHIVE[2]
            LOGS_ARCHIVE[2] = LOGS_ARCHIVE[1]
            LOGS_ARCHIVE[1] = LOGS_ARCHIVE[0]
            LOGS_ARCHIVE[0] = LOGS
        elif len(LOGS_ARCHIVE) == 9:
            LOGS_ARCHIVE.append(LOGS_ARCHIVE[8])
            LOGS_ARCHIVE[8] = LOGS_ARCHIVE[7]
            LOGS_ARCHIVE[7] = LOGS_ARCHIVE[6]
            LOGS_ARCHIVE[6] = LOGS_ARCHIVE[5]
            LOGS_ARCHIVE[5] = LOGS_ARCHIVE[4]
            LOGS_ARCHIVE[4] = LOGS_ARCHIVE[3]
            LOGS_ARCHIVE[3] = LOGS_ARCHIVE[2]
            LOGS_ARCHIVE[2] = LOGS_ARCHIVE[1]
            LOGS_ARCHIVE[1] = LOGS_ARCHIVE[0]
            LOGS_ARCHIVE[0] = LOGS
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

















# ----------------------------------------------------------------------------------------------------------------------

@router.callback_query(F.data == 'record.help')
async def help(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.helpCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    USE_SECOND = ''

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="record.recordLogs"))
    builder.row(types.InlineKeyboardButton(text="🛜 Проблема Wifi", callback_data="record.helpWifi"))
    builder.row(types.InlineKeyboardButton(text="🚳 Расслабить колеса", callback_data="record.helpRelax"))
    builder.row(types.InlineKeyboardButton(text="🔴 Не уходит крит", callback_data="record.helpBadKrit"))
    builder.row(types.InlineKeyboardButton(text="🚷 Неисправность парктроников", callback_data="record.helpParktroniks"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🛟 Помощь\n\n"
             f"📝 Выберите вашу проблему или напишите текстом, что у вас произошло, если нету соответствующей кнопки",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())


@router.callback_query(F.data == 'record.helpWifi')
async def helpWifi(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.helpCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    USE_SECOND = ''

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="record.help"))
    builder.row(types.InlineKeyboardButton(text="🛜 Не работает WiFi", callback_data="record.helpWifiNotWorking"))
    builder.row(types.InlineKeyboardButton(text="🛜 Пропал WiFi", callback_data="record.helpWifiMissing"))
    builder.row(types.InlineKeyboardButton(text="🛜 Глушилка, WiFi не работает", callback_data="record.helpWifiGlushilka"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🛟 Помощь\n\n"
             f"📝 Выберите вашу проблему или напишите текстом, что у вас произошло, если нету соответствующей кнопки",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())






@router.callback_query(F.data == 'record.helpCheck')
async def helpCheck(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.helpCheck'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="record.help"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    SENIORS = ast.literal_eval(DATA_SERVER[5])

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ <b>Тикет создан</b>\n\n"
             f"Ожидай помощи, я сообщу, когда придет помощь",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
    TIME = int(time.time())
    await database.addNewData('helps', 'tg_id_creator, tg_id_worker, text, time_create, time_done, type, status, message_id', f"'{message.from_user.id}', '0', '{message.text}', '{TIME}', '0', 'OTHER', '1', '0'")
    ID = await database.sqlRequest('SELECT * FROM helps ORDER BY id DESC LIMIT 1;')
    ID = ID[0]

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Готово", callback_data=f"record.HELPDONE-{ID[0]}"))
    builder.row(types.InlineKeyboardButton(text="Управлять роботом", url=f"https://remote.sdc.yandex-team.ru/rovers/a{ROBOT_INFO[0]}"))
    builder.add(types.InlineKeyboardButton(text="Prelauncher", url=f"https://a{ROBOT_INFO[0]}.launcher.sdc.yandex.net/prelauncher/"))


    MESSAGE = await bot.send_message(
        chat_id='-1003473617145',
        text=f'🤖 <b>A{ROBOT_INFO[0]}</b> • Прочее\n\n{SENIORS[DATA_USER[19]]} к тебе обращаются за помощью!\n\n<blockquote>{message.text}</blockquote>',
        reply_markup=builder.as_markup(),
    )
    await database.setData('helps', 'id', f"'{ID[0]}'", 'message_id', f"'{MESSAGE.message_id}'")







@router.callback_query(F.data == 'record.helpParktroniks')
async def helpParktroniks(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.help'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="record.help"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    SENIORS = ast.literal_eval(DATA_SERVER[5])

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ <b>Тикет создан</b>\n\n"
             f"Ожидай помощи, я сообщу, когда придет помощь",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
    TIME = int(time.time())
    await database.addNewData('helps', 'tg_id_creator, tg_id_worker, text, time_create, time_done, type, status, message_id', f"'{message.from_user.id}', '0', '🚷 Неисправность парктроников', '{TIME}', '0', 'PARKTRONIKS', '1', '0'")
    ID = await database.sqlRequest('SELECT * FROM helps ORDER BY id DESC LIMIT 1;')
    ID = ID[0]

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Готово", callback_data=f"record.HELPDONE-{ID[0]}"))
    builder.row(types.InlineKeyboardButton(text="Управлять роботом", url=f"https://remote.sdc.yandex-team.ru/rovers/a{ROBOT_INFO[0]}"))


    MESSAGE = await bot.send_message(
        chat_id='-1003473617145',
        text=f'🤖 <b>A{ROBOT_INFO[0]}</b> • 🚷 Неисправность парктроников\n\n{SENIORS[DATA_USER[19]]} парктроники некорректно работают, помоги ему!',
        reply_markup=builder.as_markup(),
    )
    await database.setData('helps', 'id', f"'{ID[0]}'", 'message_id', f"'{MESSAGE.message_id}'")






@router.callback_query(F.data == 'record.helpBadKrit')
async def helpBadKrit(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.help'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="record.help"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    SENIORS = ast.literal_eval(DATA_SERVER[5])

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ <b>Тикет создан</b>\n\n"
             f"Ожидай помощи, я сообщу, когда придет помощь",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
    TIME = int(time.time())
    await database.addNewData('helps', 'tg_id_creator, tg_id_worker, text, time_create, time_done, type, status, message_id', f"'{message.from_user.id}', '0', '🔴 Не уходит крит', '{TIME}', '0', 'BAD CRIT', '1', '0'")
    ID = await database.sqlRequest('SELECT * FROM helps ORDER BY id DESC LIMIT 1;')
    ID = ID[0]

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Готово", callback_data=f"record.HELPDONE-{ID[0]}"))
    builder.row(types.InlineKeyboardButton(text="Управлять роботом", url=f"https://remote.sdc.yandex-team.ru/rovers/a{ROBOT_INFO[0]}"))


    MESSAGE = await bot.send_message(
        chat_id='-1003473617145',
        text=f'🤖 <b>A{ROBOT_INFO[0]}</b> • 🔴 Не уходит крит\n\n{SENIORS[DATA_USER[19]]} крит не уходит, помоги ему!',
        reply_markup=builder.as_markup(),
    )
    await database.setData('helps', 'id', f"'{ID[0]}'", 'message_id', f"'{MESSAGE.message_id}'")







@router.callback_query(F.data == 'record.helpRelax')
async def helpRelax(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.help'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="record.help"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    SENIORS = ast.literal_eval(DATA_SERVER[5])

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ <b>Тикет создан</b>\n\n"
             f"Ожидай помощи, я сообщу, когда придет помощь",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
    TIME = int(time.time())
    await database.addNewData('helps', 'tg_id_creator, tg_id_worker, text, time_create, time_done, type, status, message_id', f"'{message.from_user.id}', '0', '🚳 Расслабить колеса', '{TIME}', '0', 'RELAX', '1', '0'")
    ID = await database.sqlRequest('SELECT * FROM helps ORDER BY id DESC LIMIT 1;')
    ID = ID[0]

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Готово", callback_data=f"record.HELPDONE-{ID[0]}"))
    builder.row(types.InlineKeyboardButton(text="Управлять роботом", url=f"https://remote.sdc.yandex-team.ru/rovers/a{ROBOT_INFO[0]}"))


    MESSAGE = await bot.send_message(
        chat_id='-1003473617145',
        text=f'🤖 <b>A{ROBOT_INFO[0]}</b> • 🚳 Расслабить колеса\n\n{SENIORS[DATA_USER[19]]} расслабь колеса, помоги ему!',
        reply_markup=builder.as_markup(),
    )
    await database.setData('helps', 'id', f"'{ID[0]}'", 'message_id', f"'{MESSAGE.message_id}'")



@router.callback_query(F.data == 'record.helpWifiGlushilka')
async def helpWifiGlushilka(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.help'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="record.help"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    SENIORS = ast.literal_eval(DATA_SERVER[5])

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ <b>Тикет создан</b>\n\n"
             f"Ожидай помощи, я сообщу, когда придет помощь",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
    TIME = int(time.time())
    await database.addNewData('helps', 'tg_id_creator, tg_id_worker, text, time_create, time_done, type, status, message_id', f"'{message.from_user.id}', '0', '🛜 Глушилка, WiFi не работает', '{TIME}', '0', 'WIFI GLUSLKA', '1', '0'")
    ID = await database.sqlRequest('SELECT * FROM helps ORDER BY id DESC LIMIT 1;')
    ID = ID[0]

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Готово", callback_data=f"record.HELPDONE-{ID[0]}"))
    builder.row(types.InlineKeyboardButton(text="Prelauncher", url=f"https://a{ROBOT_INFO[0]}.launcher.sdc.yandex.net/prelauncher/"))


    MESSAGE = await bot.send_message(
        chat_id='-1003473617145',
        text=f'🤖 <b>A{ROBOT_INFO[0]}</b> • 🛜 Глушилка, WiFi не работает\n\n{SENIORS[DATA_USER[19]]} человек поймал глушилку, помоги ему!',
        reply_markup=builder.as_markup(),
    )
    await database.setData('helps', 'id', f"'{ID[0]}'", 'message_id', f"'{MESSAGE.message_id}'")



@router.callback_query(F.data == 'record.helpWifiMissing')
async def helpWifiMissing(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.help'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="record.help"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    SENIORS = ast.literal_eval(DATA_SERVER[5])

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ <b>Тикет создан</b>\n\n"
             f"Ожидай помощи, я сообщу, когда придет помощь",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
    TIME = int(time.time())
    await database.addNewData('helps', 'tg_id_creator, tg_id_worker, text, time_create, time_done, type, status, message_id', f"'{message.from_user.id}', '0', '🛜 Пропал WiFi', '{TIME}', '0', 'WIFI MISSING', '1', '0'")
    ID = await database.sqlRequest('SELECT * FROM helps ORDER BY id DESC LIMIT 1;')
    ID = ID[0]

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Готово", callback_data=f"record.HELPDONE-{ID[0]}"))
    builder.row(types.InlineKeyboardButton(text="Prelauncher", url=f"https://a{ROBOT_INFO[0]}.launcher.sdc.yandex.net/prelauncher/"))


    MESSAGE = await bot.send_message(
        chat_id='-1003473617145',
        text=f'🤖 <b>A{ROBOT_INFO[0]}</b> • 🛜 Пропал WiFi\n\n{SENIORS[DATA_USER[19]]} у человека пропал WiFi, помоги ему!',
        reply_markup=builder.as_markup(),
    )
    await database.setData('helps', 'id', f"'{ID[0]}'", 'message_id', f"'{MESSAGE.message_id}'")






@router.callback_query(F.data == 'record.helpWifiNotWorking')
async def helpWifiNotWorking(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.help'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="record.help"))
    ROBOT_INFO = ast.literal_eval(DATA_USER[8])
    SENIORS = ast.literal_eval(DATA_SERVER[5])

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"✅ <b>Тикет создан</b>\n\n"
             f"Ожидай помощи, я сообщу, когда придет помощь",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())
    TIME = int(time.time())
    await database.addNewData('helps', 'tg_id_creator, tg_id_worker, text, time_create, time_done, type, status, message_id', f"'{message.from_user.id}', '0', '🛜 Не работает WiFi', '{TIME}', '0', 'WIFI NOT WORKING', '1', '0'")
    ID = await database.sqlRequest('SELECT * FROM helps ORDER BY id DESC LIMIT 1;')
    ID = ID[0]

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ Готово", callback_data=f"record.HELPDONE-{ID[0]}"))
    builder.row(types.InlineKeyboardButton(text="Prelauncher", url=f"https://a{ROBOT_INFO[0]}.launcher.sdc.yandex.net/prelauncher/"))

    MESSAGE = await bot.send_message(
        chat_id='-1003473617145',
        text=f'🤖 <b>A{ROBOT_INFO[0]}</b> • 🛜 Не работает WiFi\n\n{SENIORS[DATA_USER[19]]} у человека не работает WiFi, помоги ему!',
        reply_markup=builder.as_markup(),
    )
    await database.setData('helps', 'id', f"'{ID[0]}'", 'message_id', f"'{MESSAGE.message_id}'")



@router.callback_query(F.data.startswith('record.HELPDONE-'))
async def HELPDONE(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'1'")
    await database.setUserID(message.from_user.id, "state", "'record.help'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    idGate = message.data.replace('record.HELPDONE-', '')
    TASK_HELP = await database.getData('helps', 'id', f"'{idGate}'")
    now = datetime.datetime.now()
    TIME = int(time.time())
    await database.setData('helps', 'id', f"'{TASK_HELP[0]}'", 'status', f"'2'")
    await database.setData('helps', 'id', f"'{TASK_HELP[0]}'", 'tg_id_worker', f"'{message.from_user.id}'")
    await database.setData('helps', 'id', f"'{TASK_HELP[0]}'", 'time_done', f"'{TIME}'")

    TIME_TO_DONE = int(time.time()) - TASK_HELP[4]

    await bot.edit_message_text(
        chat_id='-1003473617145',
        message_id=TASK_HELP[8],
        text=f'✅ Тикет закрыт за {TIME_TO_DONE} сек.',
    )

    MESSAGE = await bot.send_message(
        chat_id=TASK_HELP[1],
        text=f'✅ Помощь оказана',
    )
    await asyncio.sleep(15)
    await MESSAGE.delete()