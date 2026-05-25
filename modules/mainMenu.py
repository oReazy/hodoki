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


@router.callback_query(F.data == 'mainMenu.Show')
async def Show(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'mainMenu.Show'")
    await database.setUserID(message.from_user.id, "temporary", "''")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    if DATA_USER[16] == 0:
        builder.row(types.InlineKeyboardButton(text="Начать запись", callback_data="record.QuestionStart", style='success', icon_custom_emoji_id='5219848989494514645'))
        builder.row(types.InlineKeyboardButton(text="Последний лог", callback_data="lastlog.Show", icon_custom_emoji_id='5217616890695816378'))
        builder.add(types.InlineKeyboardButton(text="Архив логов", callback_data="archive.Show", icon_custom_emoji_id='5219952167493867867'))
    if DATA_USER[16] == 1:
        builder.row(types.InlineKeyboardButton(text="🛠 Старший смены", callback_data="senior.Show"))
    # builder.row(types.InlineKeyboardButton(text="🆕 Помощь для вечерних", callback_data="mainMenu.faq"))
    builder.row(types.InlineKeyboardButton(text="Настройки", callback_data="settings.Show", icon_custom_emoji_id='5219899605684098553'))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 Главное меню\n\n",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'mainMenu.faq')
async def faq(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'mainMenu.faq'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ Назад", callback_data="mainMenu.Show"))
    builder.row(types.InlineKeyboardButton(text="⚙️ Перейти в настройки", callback_data="settings.Show"))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🆕 Помощь для вечерних\n\n"
             f"В нашей работе помощь всегда нужна — включить WiFi, расслабить колеса или вылечить криты. Теперь вы можете это делать в два клика! Старшие получают уведомление с управлением робота, после того, как старшие смены обработают ваш запрос, вам придет уведомление о выполненной работе. Выбирайте свое смещение и включайте помощь!",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())



@router.callback_query(F.data == 'mainMenu.faq1')
async def faq(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getData('settings', 'id', "'1'")
    await database.setUserID(message.from_user.id, "tg_answer", "'0'")
    await database.setUserID(message.from_user.id, "state", "'mainMenu.faq1'")
    DATA_USER = await database.getUserID(message.from_user.id)

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="mainMenu.Show", icon_custom_emoji_id='5220091062441251597'))

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    MAIN = await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=f"🎯 » 🔰 FAQ\n\n"
             f"<b>Начало записи</b>\n"
             f"Начать запись логов очень легко и для этого необходимо нажать на зеленую кнопку на главной странице бота. Затем выберите робота, на котором будете работать или можете выбрать из истории. Далее в зависимости от шаблона у вас будут разные вопросы: для МЛП будет указание маршрута, для ходоков указание локации. После первоначальной настройки вы переходите на экран с заполнение логов!",
        message_id=DATA_USER[2],
        reply_markup=builder.as_markup())