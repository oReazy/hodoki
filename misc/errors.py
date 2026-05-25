
import asyncio, logging, time, states, ast, datetime

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types, html, F, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

async def statisticsInc(bot: Bot):
    SETTINGS = await database.getData('settings', 'id', '1')
    ERRORS = ast.literal_eval(SETTINGS[6])
    ERRORS_WEEK = ast.literal_eval(SETTINGS[7])
    now = datetime.datetime.now()
    current_time = now.strftime("%d.%m.%d")
    # await bot.send_message(
    #     chat_id='-1003473617145',
    #     text=f'📊 <b>Статистика по инцидентам ({current_time})</b>\n\n'
    #          f'🏃‍➡️ Ходоковские роботы\n'
    #          f'<blockquote>Всего: {ERRORS[0][0] + ERRORS[0][1] + ERRORS[0][2] + ERRORS[0][3]}\n\nКриты: {ERRORS[0][0]}\nПропал Wifi: {ERRORS[0][1]}\nПересборки: {ERRORS[0][2]}\nПроблемы ICP: {ERRORS[0][3]}</blockquote>\n\n'
    #          f'🤖 MLP\n'
    #          f'<blockquote>Всего: {ERRORS[1][0] + ERRORS[1][1] + ERRORS[1][2] + ERRORS[1][3] + ERRORS[1][4] + ERRORS[1][5] + ERRORS[1][6] + ERRORS[1][7] + ERRORS[1][8]}\n\nКриты: {ERRORS[1][0]}\nПропал Wifi: {ERRORS[1][1]}\nПересборки: {ERRORS[1][2]}\nПроблемы ICP: {ERRORS[1][3]}\nПроблемы с припятствием: {ERRORS[1][4]}\nПроблемы ПП, РПП: {ERRORS[1][5]}\nОстановки без причины: {ERRORS[1][6]}\nСход с маршрута: {ERRORS[1][7]}\nМЛП не стартует: {ERRORS[1][8]}</blockquote>'
    # )
    ERRORS_WEEK[0][0] = ERRORS_WEEK[0][0] + ERRORS[0][0]
    ERRORS_WEEK[0][1] = ERRORS_WEEK[0][1] + ERRORS[0][1]
    ERRORS_WEEK[0][2] = ERRORS_WEEK[0][2] + ERRORS[0][2]
    ERRORS_WEEK[0][3] = ERRORS_WEEK[0][3] + ERRORS[0][3]
    ERRORS_WEEK[1][0] = ERRORS_WEEK[1][0] + ERRORS[1][0]
    ERRORS_WEEK[1][1] = ERRORS_WEEK[1][1] + ERRORS[1][1]
    ERRORS_WEEK[1][2] = ERRORS_WEEK[1][2] + ERRORS[1][2]
    ERRORS_WEEK[1][3] = ERRORS_WEEK[1][3] + ERRORS[1][3]
    ERRORS_WEEK[1][4] = ERRORS_WEEK[1][4] + ERRORS[1][4]
    ERRORS_WEEK[1][5] = ERRORS_WEEK[1][5] + ERRORS[1][5]
    ERRORS_WEEK[1][6] = ERRORS_WEEK[1][6] + ERRORS[1][6]
    ERRORS_WEEK[1][7] = ERRORS_WEEK[1][7] + ERRORS[1][7]
    ERRORS_WEEK[1][8] = ERRORS_WEEK[1][8] + ERRORS[1][8]
    NEW_MASSIVE = [[0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0 , 0, 0]]
    await database.setData('settings', 'id', "'1'", 'errors', f'\"{NEW_MASSIVE}\"')
    await database.setData('settings', 'id', "'1'", 'errors_week', f'\"{ERRORS_WEEK}\"')



async def statisticsIncWeek(bot: Bot):
    SETTINGS = await database.getData('settings', 'id', '1')
    ERRORS = ast.literal_eval(SETTINGS[7])
    now = datetime.datetime.now()
    current_time = now.strftime("%d.%m.%d")
    await bot.send_message(
        chat_id='-1003473617145',
        text=f'📊 <b>Статистика по инцидентам за неделю (ПН - ВС)</b>\n\n'
             f'🏃‍➡️ Ходоковские роботы\n'
             f'<blockquote>Всего: {ERRORS[0][0] + ERRORS[0][1] + ERRORS[0][2] + ERRORS[0][3]}\n\nКриты: {ERRORS[0][0]}\nПропал Wifi: {ERRORS[0][1]}\nПересборки: {ERRORS[0][2]}\nПроблемы ICP: {ERRORS[0][3]}</blockquote>\n\n'
             f'🤖 MLP\n'
             f'<blockquote>Всего: {ERRORS[1][0] + ERRORS[1][1] + ERRORS[1][2] + ERRORS[1][3] + ERRORS[1][4] + ERRORS[1][5] + ERRORS[1][6] + ERRORS[1][7] + ERRORS[1][8]}\n\nКриты: {ERRORS[1][0]}\nПропал Wifi: {ERRORS[1][1]}\nПересборки: {ERRORS[1][2]}\nПроблемы ICP: {ERRORS[1][3]}\nПроблемы с припятствием: {ERRORS[1][4]}\nПроблемы ПП, РПП: {ERRORS[1][5]}\nОстановки без причины: {ERRORS[1][6]}\nСход с маршрута: {ERRORS[1][7]}\nМЛП не стартует: {ERRORS[1][8]}</blockquote>'
    )
    NEW_MASSIVE = [[0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0 , 0, 0]]
    await database.setData('settings', 'id', "'1'", 'errors_week', f'\"{NEW_MASSIVE}\"')