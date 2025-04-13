import config
import asyncio
from app.database.models import async_main

from app.user.handlers import router
from aiogram import Bot, Dispatcher

async def main():
    await async_main()
    #Включение бота
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()

    #Настройка Router
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


