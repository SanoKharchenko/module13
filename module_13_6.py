from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
kb.insert(button1)
kb.insert(button2)

kb1 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button4 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
kb1.insert(button3)
kb1.insert(button4)


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Рассчитать")
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=kb1)


@dp.callback_query_handler(text='calories')
async def set_age(call: types.callback_query):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await call.UserState.age.set()


@dp.callback_query_handler(text="formulas")
async def get_formulas(call: types.callback_query):
    await call.message.answer("10 * вес (кг) + 6,25 * рост (см) - 5 * возраст (г) + 5", reply_markup=kb1)
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma_caloriy = 10 * float(data["weight"]) + 6.25 * float(data["growth"]) - 5 * int(data["age"]) + 5
    await message.answer(f"Ваша норма калорий: {norma_caloriy}")
    await state.finsh()


@dp.message_handler()
async def all_massages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
