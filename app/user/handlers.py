import json
from datetime import datetime

from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router, F
from sqlalchemy import update

from app.database.models import async_session, User
from app.user.func import get_currency_rates, get_yahoo_data, get_crypto_data, get_moex_data, get_fear_and_greed_index
from app.addons.utilits import format_change
from app.user import keyboard as kb
import app.database.requests as rq


router = Router()

with open("/Users/denstep256/Desktop/news_bot/app/addons/texts.json", encoding="utf-8") as file_handler:
    text_mess = json.load(file_handler)
    texts_for_bot = text_mess

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user_start(message.from_user.id,
                            message.from_user.username,
                            message.from_user.first_name,
                            datetime.now())
    await message.answer(texts_for_bot["start_message"], parse_mode='HTML', reply_markup=kb.main)

@router.message(F.text == '📧Получить отчет 📧')
async def send_news(message: Message):
    currencies = get_currency_rates()
    cryptos = get_crypto_data()
    fng_index = get_fear_and_greed_index()
    moex_data = get_moex_data()
    yahoo_data = get_yahoo_data()
    user_time = await rq.get_user_time(message.from_user.id)

    news_message = (
        "*Ежедневный финансовый обзор*\n\n"
        "🌍 *Курсы валют*:\n"
        f"- 💵 **Доллар**: {currencies['USD']['Value']} ₽ ({format_change(currencies['USD']['Value'] - currencies['USD']['Previous'])})\n"
        f"- 💶 **Евро**: {currencies['EUR']['Value']} ₽ ({format_change(currencies['EUR']['Value'] - currencies['EUR']['Previous'])})\n"
        f"- 🇨🇳 **Юань**: {currencies['CNY']['Value']} ₽ ({format_change(currencies['CNY']['Value'] - currencies['CNY']['Previous'])})\n\n"
        "📉 *Криптовалюты*:\n"
        f"- 🌈 **Bitcoin**: {cryptos['BTC']['price']:.2f} $ ({format_change(cryptos['BTC']['percent_change_24h'])})\n"
        f"- 🦴 **Ethereum**: {cryptos['ETH']['price']:.2f} $ ({format_change(cryptos['ETH']['percent_change_24h'])})\n"
        f"- 🪙 **XRP**: {cryptos['XRP']['price']:.2f} $ ({format_change(cryptos['XRP']['percent_change_24h'])})\n"
        f"- 🌞 **Solana**: {cryptos['SOL']['price']:.2f} $ ({format_change(cryptos['SOL']['percent_change_24h'])})\n"
        f"- 🏖 **BNB**: {cryptos['BNB']['price']:.2f} $ ({format_change(cryptos['BNB']['percent_change_24h'])})\n"
        f"- 🌐 **Toncoin**: {cryptos['TON']['price']:.2f} $ ({format_change(cryptos['TON']['percent_change_24h'])})\n"
        f"- 💸 **TRUMP**: {cryptos['TRUMP']['price']:.2f} $ ({format_change(cryptos['TRUMP']['percent_change_24h'])})\n\n"
        "📊 *Индексы*:\n"
        f"- 😱 **Индекс страха и жадности**: {fng_index['value']} ({fng_index['value_classification']})\n"
        f"- 📈 **IMOEX**: {moex_data['IMOEX']['price']} ₽ ({format_change(moex_data['IMOEX']['change'])})\n"
        f"- 📈 **S&P 500**: {yahoo_data['S&P 500']['price']:.2f} $ ({format_change(yahoo_data['S&P 500']['change'])})\n\n"
        "📉 *Акции*:\n"
        f"- 🏦 **Сбербанк**: {moex_data['SBER']['price']} ₽ ({format_change(moex_data['SBER']['change'])})\n"
        f"- ⛽ **Газпром**: {moex_data['GAZP']['price']} ₽ ({format_change(moex_data['GAZP']['change'])})\n"
        f"- ⛽ **Лукойл**: {moex_data['LKOH']['price']} ₽ ({format_change(moex_data['LKOH']['change'])})\n"
        f"- 🌐 **Яндекс**: {moex_data['YDEX']['price']} ₽ ({format_change(moex_data['YDEX']['change'])})\n"
        f"- 🛢 **Роснефть**: {moex_data['ROSN']['price']} ₽ ({format_change(moex_data['ROSN']['change'])})\n\n"
        f"- 🍏 **Apple**: {yahoo_data['Apple']['price']:.2f} $ ({format_change(yahoo_data['Apple']['change'])})\n"
        f"- 🚗 **Tesla**: {yahoo_data['Tesla']['price']:.2f} $ ({format_change(yahoo_data['Tesla']['change'])})\n"
        f"- 💻 **Nvidia**: {yahoo_data['Nvidia']['price']:.2f} $ ({format_change(yahoo_data['Nvidia']['change'])})\n"
        f"- 🔍 **Google**: {yahoo_data['Google']['price']:.2f} $ ({format_change(yahoo_data['Google']['change'])})\n"
        f"- 📦 **Amazon**: {yahoo_data['Amazon']['price']:.2f} $ ({format_change(yahoo_data['Amazon']['change'])})\n\n"
        f"🕒 *Обновление:* {user_time}"
    )


    await message.answer(news_message, parse_mode='Markdown')

@router.message(F.text == 'Настройки')
async def settings(message: Message):
    await message.answer('Выберите часовой пояс (по умолчанию - МСК(UTC+3))', parse_mode='HTML', reply_markup=kb.time_zone_keyboard)

@router.message(F.text == '🏠Иркутск (UTC+8)')
async def change_timezone_irk(message: Message):
    tg_id = message.from_user.id  # Получаем tg_id пользователя

    async with async_session() as session:
        # Обновляем поле time_utc для данного пользователя
        query = update(User).where(User.tg_id == tg_id).values(time_utc="+8")
        await session.execute(query)
        await session.commit()

    await message.answer('Выбранный часовой пояс: Иркутск (UTC+8)', parse_mode='HTML', reply_markup=kb.main)

@router.message(F.text == '🏠МСК (UTC+3)')
async def change_timezone_irk(message: Message):
    tg_id = message.from_user.id  # Получаем tg_id пользователя

    async with async_session() as session:
        # Обновляем поле time_utc для данного пользователя
        query = update(User).where(User.tg_id == tg_id).values(time_utc="+3")
        await session.execute(query)
        await session.commit()

    await message.answer('Выбранный часовой пояс: МСК (UTC+3)', parse_mode='HTML', reply_markup=kb.main)

@router.message(F.text == 'Вернуться в меню')
async def change_timezone_irk(message: Message):
    await message.answer('Вы вернулись в меню', parse_mode='HTML', reply_markup=kb.main)