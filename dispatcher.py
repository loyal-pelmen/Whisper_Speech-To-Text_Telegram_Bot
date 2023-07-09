import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from filters import IsOwner, IsUser
from logging.handlers import RotatingFileHandler
from config import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK, MAXCONNECTIONS, UPDATESPENDING, LOG_LEVEL, OWNERS_IDS, ALLOWED_IDS


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
    folder_path = './voices'  # замени на свой путь к папке

    file_paths = map(lambda filename: os.path.join(folder_path, filename), os.listdir(folder_path))
    list(map(os.remove, file_paths))


    if WEBHOOK:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=UPDATESPENDING, max_connections=MAXCONNECTIONS)
    dp.filters_factory.bind(IsOwner)
    dp.filters_factory.bind(IsUser)


    if 1 in OWNERS_IDS:
        logging.info('У вас указана 1 в OWNERS_IDS. Это даёт доступ всем пользователям к админским функциям')

    if 1 in ALLOWED_IDS:
        logging.info('У вас указана 1 в ALLOWED_IDS. Это даёт доступ всем пользователям к пользовательским функциям')

    if not (OWNERS_IDS or ALLOWED_IDS):
        logging.warning('У вас не указано id админов и пользователей - бот не доступен никому.')
    if not OWNERS_IDS:
        logging.warning('У вас не указано id админов - админские функции не доступны никому.')



async def stop():
    if WEBHOOK:
        await bot.delete_webhook()


