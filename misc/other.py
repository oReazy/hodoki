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

from modules import database, registration, mainMenu, settings, record, lastlog, archive
# from modules import senior
from misc import logout, errors

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

# bot = Bot(token="8542519204:AAGILv1SZg-EN6MDG57H7lvvFBIGHiErJp4", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot = Bot(token="8416280540:AAG7gE3IMe_rLpkHw2iEF4p6RfoekelVmQc", default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

dp = Dispatcher()
dp.include_routers(registration.router)
dp.include_routers(mainMenu.router)
dp.include_routers(settings.router)
dp.include_routers(record.router)
dp.include_routers(lastlog.router)
dp.include_routers(archive.router)
# dp.include_routers(senior.router)

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

logging.basicConfig(level=logging.INFO)
# logging.disable(level=logging.CRITICAL)
functions = states.STATES

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

@dp.message(F.text, Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    if await database.getDataMultiCount('users', 'tg_id', f'{message.from_user.id}') == 0:
        await registration.registation_0(message, bot)
        return


@dp.message(F.text, Command("new_message"))
async def cmd_newMessage(message: types.Message, bot: Bot):
    if await database.getDataMultiCount('users', 'tg_id', f'{message.from_user.id}') == 0:
        await registration.registation_0(message, bot)
        return
    else:
        await database.setUserID(message.from_user.id, 'tg_online', f"'1'")
        NEW_MESSAGE = await bot.send_message(
            chat_id=message.from_user.id,
            text='📶 Подключаемся к боту...'
        )
        await database.setUserID(message.from_user.id, "tg_mainMessage", f"'{NEW_MESSAGE.message_id}'")
        await database.setUserID(message.from_user.id, 'tg_lastMessage', f"'{time.time()}'")
        await mainMenu.Show(message, bot)


@dp.message(F.text, Command("send_me_email"))
async def cmd_newMessage(message: types.Message, bot: Bot):
    await message.answer_photo(
        text='🎄 <b>С наступающим 2026 годом</b>\n\n'
             'Этот год стал самым необычным, интересным и даже увлекательным. За этот год мы сделали много интересных вещей. Помогали картографии, обучали новеньких. '
             'Нами интересовались все, ведь мы центр притяжения и надеюсь, что следующий год станет еще лучше для всей нашей команды — <b>Ходоков</b>\n\n'
             'Чтобы в новом году у вас не ломались джои, не болели и еще чаще встречались со своими коллегами не на работе, а в баре.\n\n'
             '🌍 Dislog » вместе с вами в 2026!',
        photo='AgACAgIAAxkBAAEIlV1pVSjBbiNRFZU4gmPENcDPEfXOxAAC1hBrG3-wqErqOt-Q0Mf6lAEAAwIAA3kAAzgE'
    )


@dp.message(F.text, Command("send_all_email"))
async def cmd_newMessage(message: types.Message, bot: Bot):
    await message.answer_photo(
        text='🎄 <b>С наступающим 2026 годом</b>\n\n'
             'Этот год стал самым необычным, интересным и даже увлекательным. За этот год мы сделали много интересных вещей. Помогали картографии, обучали новеньких. '
             'Нами интересовались все, ведь мы центр притяжения и надеюсь, что следующий год станет еще лучше для всей нашей команды — <b>Ходоков</b>\n\n'
             'Чтобы в новом году у вас не ломались джои, не болели и еще чаще встречались со своими коллегами не на работе, а в баре.\n\n'
             '🌍 Dislog » вместе с вами в 2026!',
        photo='AgACAgIAAxkBAAEIlV1pVSjBbiNRFZU4gmPENcDPEfXOxAAC1hBrG3-wqErqOt-Q0Mf6lAEAAwIAA3kAAzgE'
    )


@dp.message()
async def any(message: types.Message, bot: Bot):
    NUM = int(message.chat.id)
    if NUM == -1003473617145:
        print('ignore')
    else:
        await database.setUserID(message.from_user.id, 'tg_lastMessage', f"'{time.time()}'")
        DATA_USER = await database.getUserID(message.from_user.id)
        if DATA_USER[3] == 1:
            await message.delete()
            match DATA_USER[4]:
                case 'registration.registration_1_check': await registration.registration_1_check(message, bot)
                case 'record.StartRobotCheck': await record.StartRobotCheck(message, bot)
                case 'record.StartRouteCheck': await record.StartRouteCheck(message, bot)
                case 'record.recordLogsText': await record.recordLogsText(message, bot)
                case 'record.StartLocationCheck': await record.StartLocationCheck(message, bot)
                case 'record.stopBatteryCheck': await record.stopBatteryCheck(message, bot)
                case 'record.stopSSDCheck': await record.stopSSDCheck(message, bot)
                case 'record.stopDistanceCheck': await record.stopDistanceCheck(message, bot)
                case 'record.helpCheck': await record.helpCheck(message, bot)
                case 'settings.buttonsAddCheck': await settings.buttonsAddCheck(message, bot)
                case 'settings.buttonsAddCheck2': await settings.buttonsAddCheck2(message, bot)
                case 'settings.buttonsAddCategoryCheck': await settings.buttonsAddCategoryCheck(message, bot)
                case 'settings.buttonsAddCategoryCheck2': await settings.buttonsAddCategoryCheck2(message, bot)
                case 'settings.buttonsEditCheck': await settings.buttonsEditCheck(message, bot)
                # case 'senior.LocationsAddCheck': await senior.LocationsAddCheck(message, bot)
                # case 'senior.LocationsAddGeoCheck': await senior.LocationsAddGeoCheck(message, bot)
        else:
            await message.delete()

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(logout.logoutServer, "cron", hour=2, args=(bot,))
    scheduler.add_job(errors.statisticsInc, "cron", hour=23, minute=0, args=(bot,))
    scheduler.add_job(errors.statisticsIncWeek, "cron", day_of_week=6, hour=23, minute=1, args=(bot,))
    scheduler.start()
    print("\033[38m[\033[32m!\033[38m][\033[33mDEBUG\033[38m] Бот запущен!\033[38m")
    await dp.start_polling(bot)

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

if __name__ == "__main__":
    asyncio.run(main())