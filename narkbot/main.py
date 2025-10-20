import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

TOKEN = "ТОКЕН_ТВОЕГО_БОТА"  # вставь свой токен от @BotFather
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Память городов (временная, можно заменить на базу)
user_cities = {}

# Главное меню
def main_menu():
    buttons = [
        [KeyboardButton("📍 ЛОКАЦИИ"), KeyboardButton("🎁 БОНУСЫ")],
        [KeyboardButton("📜 ПРАВИЛА"), KeyboardButton("💬 ОТЗЫВЫ")],
        [KeyboardButton("🆘 ПОДДЕРЖКА")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_city = user_cities.get(user_id, "Киев")

    photo = InputFile("black.jpg")  # просто чёрная картинка в папке с ботом
    text = (
        f"Ваша страна: Украина\n"
        f"Ваш город: {user_city}\n\n"
        f"Пригласи друга и получи бонус: https://t.me/kittynarkbot?start=r_1258"
    )

    await message.answer_photo(photo=photo, caption=text, reply_markup=main_menu())

# Локации
@dp.message_handler(lambda msg: msg.text == "📍 ЛОКАЦИИ")
async def locations(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Киев", "Львов", "Одесса", "Харьков", "Назад")
    await message.answer("Выберите ваш город:", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text in ["Киев", "Львов", "Одесса", "Харьков"])
async def set_city(message: types.Message):
    user_cities[message.from_user.id] = message.text
    await message.answer(f"✅ Город установлен: {message.text}", reply_markup=main_menu())

@dp.message_handler(lambda msg: msg.text == "Назад")
async def back_to_menu(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu())

# Остальные кнопки
@dp.message_handler(lambda msg: msg.text == "🎁 БОНУСЫ")
async def bonuses(message: types.Message):
    await message.answer("💎 Бонусы будут доступны позже!")

@dp.message_handler(lambda msg: msg.text == "📜 ПРАВИЛА")
async def rules(message: types.Message):
    await message.answer("📜 Правила:\n1. Не нарушай.\n2. Уважай других пользователей.")

@dp.message_handler(lambda msg: msg.text == "💬 ОТЗЫВЫ")
async def reviews(message: types.Message):
    await message.answer("💬 Отзывы можно оставить здесь: @your_feedback_channel")

@dp.message_handler(lambda msg: msg.text == "🆘 ПОДДЕРЖКА")
async def support(message: types.Message):
    await message.answer("🆘 Поддержка: @your_support_username")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
