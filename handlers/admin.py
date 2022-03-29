from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from create_bot import bot
from data_base import sqlite_db
from data_base.sqlite_db import sql_add_comment
from keyboards.admin_kb import button_case_admin

ID = None


# from create_bot import dp
class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    dеscription = State()
    price = State()


# Получаем ID текущего модератора
# @dp.message_handler(commands="Модератор", is_chat_admin=True)
async def make_change_command(message: Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id, "Что хозяин надо?", reply_markup=button_case_admin
    )
    await message.delete()


# Начало диалога с админом и загрузки нового изделия
# @dp.message_handler(commands="Загрузить", state=None)
async def cm_start(message: Message):
    if message.from_user.id == ID:
        await FSMadmin.photo.set()
        await message.reply("Загрузи фото")


# Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=["photo"], state=FSMadmin.photo)
async def load_photo(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
            await FSMadmin.next()
            await message.reply("Введи название модели")


# Ловим второй ответ
# @dp.message_handler(state=FSMadmin.name)
async def load_name(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["name"] = message.text
            await FSMadmin.next()
            await message.reply("Введи описание модели")


# Ловим третий ответ
# @dp.message_handler(state=FSMadmin.description)
async def load_description(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["dеscription"] = message.text
            await FSMadmin.next()
            await message.reply("Укажи цену модели")


# Ловим последний ответ
# @dp.message_handler(state=FSMadmin.price)
async def load_price(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["price"] = float(message.text)

        await sql_add_comment(state)

        await state.finish()


# Выход из состояний
# @dp.message_handler(commands="Отмена", state="*")
# @dp.message_handler(Text(equals="Отмена", ignor_case=True), state="*")
async def cancel_handler(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("Внесение новой модели отменено")


# @dp.message_handler(commands="Удалить")
async def delete_model(message: Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_all()
        for ret in read:
            await bot.send_photo(
                message.from_user.id,
                ret[0],
                f"{ret[1]} Описание:{ret[2]} Цена: {ret[3]}",
            )
            await bot.send_message(
                message.from_user.id,
                text="Удаление модели",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        f"Удалить {ret[1]}", callback_data=f"del {ret[1]}"
                    )
                ),
            )


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith("del "))
async def del_callback_run(callback_query: CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(
        text=f"{callback_query.data.replace('del', '')} удалена.", show_alert=True
    )


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):

    dp.register_message_handler(
        make_change_command, commands=["Модератор"], is_chat_admin=True
    )

    dp.register_message_handler(cm_start, commands=["Загрузить"], state=None)

    dp.register_message_handler(
        load_photo, content_types=["photo"], state=FSMadmin.photo
    )

    dp.register_message_handler(load_name, state=FSMadmin.name)

    dp.register_message_handler(load_description, state=FSMadmin.dеscription)

    dp.register_message_handler(load_price, state=FSMadmin.price)

    dp.register_message_handler(cancel_handler, commands=["Отмена"], state="*")

    dp.register_message_handler(delete_model, commands=["Удалить"])

    dp.register_callback_query_handler(
        del_callback_run, lambda x: x.data and x.data.startswith("del ")
    )
