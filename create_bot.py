# import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

# logging.basicConfig(
#     format="%(filename)s [LINE:%(lineno)d] #%(levelname)-8s\
#     [%(asctime)s]  %(message)s",
#     level=logging.INFO,
# )

storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
