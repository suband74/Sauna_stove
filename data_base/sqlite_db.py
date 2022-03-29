from aiogram.types import Message
import sqlite3 as sq

from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect("sauna_stove.db")
    cur = base.cursor()
    if base:
        print("Data base connected OK!")
    base.execute(
        "CREATE TABLE IF NOT EXISTS models(img TEXT, name TEXT PRIMARY KEY,\
            description TEXT, price TEXT)"
    )
    base.commit()


async def sql_add_comment(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO models VALUES (?, ?, ?, ?)", tuple(data.values()))
        base.commit()


async def sql_read_all():
    return cur.execute("SELECT * FROM models").fetchall()


async def sql_read(message: Message):
    for ret in cur.execute("SELECT * FROM models").fetchall():
        await bot.send_photo(
            message.from_user.id,
            ret[0],
            f"{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}",
        )


async def sql_delete_command(data):
    cur.execute("DELETE FROM models WHERE name == ?", (data,))
    base.commit()
