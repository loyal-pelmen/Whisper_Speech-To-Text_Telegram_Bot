import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from filters import IsOwner, IsUser
from logging.handlers import RotatingFileHandler
from config import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK, MAXCONNECTIONS, UPDATESPENDING, LOG_LEVEL


# Настроить ведение журнала
logging.basicConfig(level=LOG_LEVEL, filename='app.log')
handler = RotatingFileHandler('app.log', maxBytes=102400, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


# предпосылки
if not BOT_TOKEN:
    exit("No token provided")


# init
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# webhook settings
WEBHOOK_PATH = f'/{BOT_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


async def start(dp):
    if WEBHOOK:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=UPDATESPENDING, max_connections=MAXCONNECTIONS)
    dp.filters_factory.bind(IsOwner)
    dp.filters_factory.bind(IsUser)



async def stop():
    if WEBHOOK:
        await bot.delete_webhook()


