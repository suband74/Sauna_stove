import json
import string

from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from create_bot import bot
from data_base import sqlite_db
from keyboards.client_kb import kb_client


# @dp.message_handler(commands=["start", "help"])
async def command_start(message: Message):
    try:
        await bot.send_message(
            message.from_user.id, "Погреемся!)", reply_markup=kb_client
        )
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему")


# @dp.message_handler(commands=["Режим_работы"])
async def sauna_open_command(message: Message):
    await bot.send_message(message.from_user.id, "Пн-Пт с 9-00 до 18-00")


# @dp.message_handler(commands=["Адрес"])
async def sauna_place_command(message: Message):
    await bot.send_message(message.from_user.id, "3я Шинная 2а")


# @dp.message_handler(commands=["Модели"])
async def sauna_models_command(message: Message):
    await sqlite_db.sql_read(message)


# @dp.message_handler()
async def trash_send(message: Message):
    if {
        i.lower().translate(str.maketrans("", "", string.punctuation))
        for i in message.text.split(" ")
    }.intersection(set(json.load(open("cenz.json")))) != set():
        await message.reply("Маты запрещены")
        await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(sauna_open_command, commands=["Режим_работы"])
    dp.register_message_handler(sauna_place_command, commands=["Адрес"])
    dp.register_message_handler(sauna_models_command, commands=["Модели"])
    dp.register_message_handler(trash_send)
