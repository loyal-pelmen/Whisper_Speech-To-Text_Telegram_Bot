import openai
import logging
import tempfile
import pydub
import os
import traceback
from utils.openai_utils import transcribe_audio
from dispatcher import dp, bot
from filters import IsUser
from aiogram import types
from pathlib import Path
from config import OPENAI_TOKENS, PROXY
from moviepy.editor import VideoFileClip
from utils.my_utils import remove_token, split_text, send_err_log



@dp.message_handler(IsUser(), commands='start')
@dp.async_task
async def start(msg: types.Message):
    await msg.delete()
    await msg.answer(f'''<b>Привет, {msg.from_user.first_name}!😊 Жду аудио!</b>''', parse_mode='HTML')



@dp.message_handler(IsUser(), commands='help')
@dp.async_task
async def help(msg: types.Message):
    await msg.delete()
    await msg.answer(f'''<b>Запишите голосовое или видеосообщение и бот пришлёт расшифровку.</b>''', parse_mode='HTML')





@dp.message_handler(IsUser(), content_types=[types.ContentType.VOICE])
@dp.async_task
async def voice_message_handle(message: types.Message):
    n = 1
    for i in OPENAI_TOKENS:
        try:
            if n == 1:  #Если сообщение не отправлено или отправлено с ошибкой и требует исправления
                openai.api_key = i
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_dir = Path('./voices')
                    voice_ogg_path = tmp_dir / f"{message.from_id}-{message.message_id}voice.ogg"



                    # download
                    voice_file = await bot.get_file(message.voice.file_id)
                    await voice_file.download(voice_ogg_path)

                    # convert to mp3
                    voice_mp3_path = tmp_dir / f"{message.from_id}-{message.message_id}voice.mp3"
                    pydub.AudioSegment.from_file(voice_ogg_path).export(voice_mp3_path, format="mp3")
                    # transcribe
                    with open(voice_mp3_path, "rb") as f:
                        transcribed_text = await transcribe_audio(audio_file=f, token=i, proxy=PROXY)

                        if transcribed_text is None:
                            exit()

                text = f"{transcribed_text}"
                logging.debug(text)
                # удалить файлы
                os.remove(voice_ogg_path)
                os.remove(voice_mp3_path)

                list_of_messages = split_text(text, 4096)
                for piece in list_of_messages:
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    message = await message.reply(text=piece)
                n = 0
                break
                
        except Exception as e:

            if f'{e}' == 'You exceeded your current quota, please check your plan and billing details.':    #Нет токенов на ключе API
                await send_err_log(f'Удаляю токен {i}. Добавь новых токенов!!!')   #Оповещдаем админа о том, что удадлили api клююч и нам нужен новый
                await remove_token(i)  #Удаляем ключ api из списка
                n = 1   #Действие не удалось
                continue
            if f'{e}' == 'File is too big':
                await message.reply(text='Файл слишком большой')



            if OPENAI_TOKENS.index(i) != len(OPENAI_TOKENS) - 1:
                n = 1   #Действие не удалось
                continue
            else:
                    await message.reply(text='Произошла ошибка. Повторите попытку.')
                    logging.debug(f'{e.with_traceback}')
                    await send_err_log(f'Сообщение об ошибке не отправилось:\n{e}\n{traceback.print_exc()}')
            await send_err_log(f'{e}\n\n{traceback.print_exc()}')
            logging.debug(f'{e}\n{traceback.print_exc()}')
            try:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_dir = Path('./voices')
                    voice_ogg_path = tmp_dir / f"{message.from_id}-{message.message_id}voice.ogg"
                    voice_mp3_path = tmp_dir / f"{message.from_id}-{message.message_id}voice.mp3"

                os.remove(voice_ogg_path)
                os.remove(voice_mp3_path)
            except:
                pass





@dp.message_handler(IsUser(), content_types=types.ContentType.VIDEO_NOTE)
@dp.async_task
async def video_message_handle(message: types.Message):
    n = 1
    for i in OPENAI_TOKENS:
        try:
            if n == 1:  #Если сообщение не отправлено или отправлено с ошибкой и требует исправления
                openai.api_key = i
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_dir = Path('./voices')
                    videonote_path = tmp_dir / f"{message.from_id}-{message.message_id}video_note.mp4"



                    # download
                    voice_file = await bot.get_file(message.video_note.file_id)
                    await voice_file.download(videonote_path)
                    # convert to mp3
                    audio_path = tmp_dir / f"{message.from_id}-{message.message_id}audio_note.mp3"
                    video = VideoFileClip(str(videonote_path))
                    video.audio.write_audiofile(audio_path) # type: ignore



                    # transcribe
                    with open(audio_path, "rb") as f:
                        transcribed_text = await transcribe_audio(audio_file=f, token=i, proxy=PROXY)

                        if transcribed_text is None:
                            exit()

                text = f"{transcribed_text}"
                logging.debug(text)
                # удалить файлы
                os.remove(videonote_path)
                os.remove(audio_path)

                list_of_messages = split_text(text, 4096)
                for piece in list_of_messages:
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    message = await message.reply(text=piece)
                n = 0
                break
                
        except Exception as e:
            if f'{e}' == 'You exceeded your current quota, please check your plan and billing details.':    #Нет токенов на ключе API
                await send_err_log(f'Удаляю токен {i}. Добавь новых токенов!!!')   #Оповещдаем админа о том, что удадлили api клююч и нам нужен новый
                await remove_token(i)  #Удаляем ключ api из списка
                n = 1   #Действие не удалось
                continue
            if f'{e}' == 'File is too big':
                await message.reply(text='Файл слишком большой')


            if OPENAI_TOKENS.index(i) != len(OPENAI_TOKENS) - 1:
                n = 1   #Действие не удалось
                continue
            else:
                    await message.reply(text='Произошла ошибка. Повторите попытку.')
                    logging.debug(f'{e.with_traceback}')
                    await send_err_log(f'Сообщение об ошибке не отправилось:\n{e}\n{traceback.print_exc()}')
            await send_err_log(f'{e}\n\n{traceback.print_exc()}')
            logging.debug(f'{e}\n{traceback.print_exc()}')
            try:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_dir = Path('./voices')
                    audio_path = tmp_dir / f"{message.from_id}-{message.message_id}audio_note.mp3"

                videonote_path = tmp_dir / f"{message.from_id}-{message.message_id}video_note.mp4"
                os.remove(videonote_path)
                os.remove(audio_path)
            except:
                pass
