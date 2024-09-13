import logging

from aiogram import Bot, Dispatcher, types #executor
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
import asyncio

api = "7512843645:AAFZOEal0hggbP4UqBnkqUXMXzS-W4ZcqOo"
bot = Bot(token=api)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

async def main():
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def start(message: types.Message):
    print("Привет! Я бот помогающий твоему здоровью.")


@dp.message
async def all_messages(message: types.Message):
    print("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    asyncio.run(main())