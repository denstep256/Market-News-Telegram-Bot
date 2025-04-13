from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📧Получить отчет 📧')],
                                     [KeyboardButton(text='Настройки ')]],
                           resize_keyboard=True)

time_zone_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🏠МСК (UTC+3)')],
                                                  [KeyboardButton(text='🏠Иркутск (UTC+8)')],
                                                  [KeyboardButton(text='Вернуться в меню')]],
                                         resize_keyboard=True)