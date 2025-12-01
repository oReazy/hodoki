# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
#
# LOGS FOR YANDEX BY SDG
#
# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

import asyncio, logging, time, states, random, ast

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types, html, F
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database, registration, mainMenu, settings, record, lastlog
from misc import logout

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

bot = Bot(token="", default=DefaultBotProperties(parse_mode=ParseMode.HTML), proxy='http://proxy.server:3128')

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

dp = Dispatcher()
dp.include_routers(registration.router)
dp.include_routers(mainMenu.router)
dp.include_routers(settings.router)
dp.include_routers(record.router)
dp.include_routers(lastlog.router)

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

logging.basicConfig(level=logging.INFO)
# logging.disable(level=logging.CRITICAL)
functions = states.STATES

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

@dp.message()
async def cmd_start(message: types.Message, bot: Bot):
    if message.text == '/new_message':
        NEW_MESSAGE = await bot.send_message(
            chat_id=message.from_user.id,
            text='📶 Подключаемся к боту...'
        )
        await database.setUserID(message.from_user.id, "tg_mainMessage", f"'{NEW_MESSAGE.message_id}'")
    if await database.getDataMultiCount('users', 'tg_id', f'{message.from_user.id}') == 0:
        await registration.registation_0(message, bot)
        return
    else:
        await database.setUserID(message.from_user.id, 'tg_lastMessage', f"'{time.time()}'")
        DATA_USER = await database.getUserID(message.from_user.id)
        if DATA_USER[12] == 0:
            await database.setUserID(message.from_user.id, 'tg_online', f"'1'")
        if DATA_USER[3] == 0:
            await message.delete()
            NEW_MESSAGE = await bot.send_message(
                chat_id=message.from_user.id,
                text='📶 Подключаемся к боту...'
            )
            await database.setUserID(message.from_user.id, "tg_mainMessage", f"'{NEW_MESSAGE.message_id}'")
            await mainMenu.Show(message, bot)
        else:
            await message.delete()
            match DATA_USER[4]:
                case 'registration.registration_1_check': await registration.registration_1_check(message, bot)
                case 'record.StartRobotCheck': await record.StartRobotCheck(message, bot)
                case 'record.StartRouteCheck': await record.StartRouteCheck(message, bot)
                case 'record.recordLogsText': await record.recordLogsText(message, bot)

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(logout.logoutServer, "cron", second=0, args=(bot,))
    scheduler.start()
    print("\033[38m[\033[32m!\033[38m][\033[33mDEBUG\033[38m] Бот запущен!\033[38m")
    await dp.start_polling(bot)

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

if __name__ == "__main__":
    asyncio.run(main())