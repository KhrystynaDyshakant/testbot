import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

TOKEN = getenv("TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    buttons = [
        types.InlineKeyboardButton(text="Шукати житло", callback_data="search_apartments"),
        types.InlineKeyboardButton(text="Виставити оголошення", callback_data="post_ad"),
    ]

    keyboard = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [buttons[0]],
            [buttons[1]],
        ],
    )

    await message.answer(
        f"Привіт, {hbold(message.from_user.full_name)}! Я бот LetAFlat \n"
        "Для початку, підкажи: хочеш пошукати житло в оренду чи виставити оголошення?",
        reply_markup=keyboard,
    )

@dp.callback_query(lambda query: query.data == "search_apartments")
async def search_apartments_handler(query: CallbackQuery) -> None:
    """
    Handle the callback query for searching apartments
    """

    city_buttons = [
        types.InlineKeyboardButton(text="Київ", callback_data="city_Київ"),
        types.InlineKeyboardButton(text="Львів", callback_data="city_lviv"),
        # Add more city...
    ]

    city_keyboard = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [city_buttons[0], city_buttons[1]],  # Add more rows...
        ],
    )

    await query.message.edit_text(
        "Обери місто, в якому ти шукаєш квартиру:",
        reply_markup=city_keyboard,
    )

@dp.callback_query(lambda query: query.data.startswith("city_"))
async def city_selection_handler(query: CallbackQuery) -> None:
        """
        Handle the callback query for selecting a city
        """
        city = query.data.split("_")[1]

        district_buttons = [
            types.InlineKeyboardButton(text="Дарницький", callback_data="district_darnitskiy"),
            types.InlineKeyboardButton(text="Деснянський", callback_data="district_desnyanskiy"),
            # Add more district...
        ]

        district_keyboard = types.InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=[
                [district_buttons[0], district_buttons[1]],  # Add more rows...
            ],
        )

        await query.message.edit_text(
            f"Обери район у місті {city}:",
            reply_markup=district_keyboard,
        )

@dp.callback_query(lambda query: query.data.startswith("district_"))
async def district_selection_handler(query: CallbackQuery) -> None:
    """
    Handle the callback query for selecting a district
    """
    district = query.data.split("_")[1]

    current_text = query.message.text
    if "☑️" not in current_text:
        current_text += f"\n☑️ Обраний район: {district}"
    else:
        current_text = current_text.replace(f"☑️ Обраний район: {district}", "")

    navigation_buttons = [
        types.InlineKeyboardButton(text="Назад", callback_data="back_to_city_selection"),
        types.InlineKeyboardButton(text="Далі", callback_data="proceed_to_next_step"),
    ]

    navigation_keyboard = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [navigation_buttons[0], navigation_buttons[1]],
        ],
    )

    await query.message.edit_text(
        current_text,
        reply_markup=navigation_keyboard,
    )

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
