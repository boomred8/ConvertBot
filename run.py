import asyncio
import os
import logging
from aiogram import Bot, Dispatcher

from app.keyboards import main_reply
from main import bot_token
import app.handlers.start_handler as start_handler
import app.handlers.Profile_handler as profile_handler
import app.handlers.conversion_handler as conversion_handler


bot = Bot(token=bot_token)
dp = Dispatcher()

async def main():
    dp.include_router(start_handler.router_start)
    dp.include_router(profile_handler.profile_router)
    dp.include_router(conversion_handler.conversion_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    #logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')