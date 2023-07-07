import logging
import sys
from dispatcher import stop
from os import execl
from config import config
from aiogram import Bot
from ujson import dump


async def confupdate():
    with open('./config.json', 'w') as file:
        file.write('')
        dump(config, file)


async def remove_token(token:str):
    config['OPENAI_TOKENS'].remove(token)


def split_text(text:str, chunk_size:int) -> list[str]:
    chunks = []
    while text:
        if len(text) > chunk_size:
            chunks.append(text[0:chunk_size])
            text = text[chunk_size:]
        else:
            chunks.append(text)
            text = ''
    return chunks[::-1]


async def send_err_log(message):
    " Отправляем сообщение в бот с логами"
    try:
        for id in config['OWNERS_IDS']:
            await Bot(str(config['LOG_BOT_TOKEN'])).send_message(chat_id=id, text=message)
    except:
        pass


async def restart():
    logging.info('Бот перезагружается...')
    await stop()
    python = sys.executable
    execl(python, python, *sys.argv)