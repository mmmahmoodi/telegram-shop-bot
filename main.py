import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database.db_worker import init_db
from bot.handlers.user_handlers import router as user_router

logging.basicConfig(level=logging.INFO)


async def main():
    # راه‌اندازی دیتابیس
    await init_db()
    logging.info("✅ دیتابیس با موفقیت ساخته شد!")

    # ساخت ربات
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # ثبت روترها
    dp.include_router(user_router)

    logging.info("🤖 ربات در حال اجراست...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
