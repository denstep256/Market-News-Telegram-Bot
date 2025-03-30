from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select


async def set_user_start(tg_id, username, first_name, date_add):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user_in_user = result.scalar_one_or_none()

        if not user_in_user:
            new_user = User(
                tg_id=tg_id,
                username=username,
                first_name=first_name,
                date_add=date_add,
            )
            session.add(new_user)
            await session.commit()

async def get_user_time(user_id: int):
    async with async_session() as session:
        # Извлекаем полный объект пользователя
        query = select(User).where(User.tg_id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()  # Получаем объект пользователя

        if not user:  # Проверяем, если пользователь не найден
            return "UTC"

        time_utc = user.time_utc  # Берем значение time_utc из объекта пользователя

        if not time_utc:  # Проверка на None и пустую строку
            return "UTC"

        try:
            # Преобразуем строку в int (убираем "+" и пробелы)
            offset_hours = int(time_utc.replace("+", "").strip())
        except ValueError:
            return "UTC"  # Если произошла ошибка при преобразовании, возвращаем "UTC"

        # Рассчитываем время пользователя с учетом смещения
        user_time = datetime.now(timezone.utc) + timedelta(hours=offset_hours)

        # Возвращаем время в нужном формате
        return user_time.strftime("%Y-%m-%d %H:%M")