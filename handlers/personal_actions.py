from aiogram import types
from dispatcher import dp, handler
from config import config
from filters import IsOwner
from subprocess import call, run
from utils.my_utils import restart, confupdate



api = config['OPENAI_TOKENS']





@dp.message_handler(IsOwner(), commands=['restart'])
@dp.async_task
async def handle_restart(message: types.Message):
    await message.delete()
    await message.answer('Перезагрузка...')
    await restart()




@dp.message_handler(IsOwner(), commands=["ping"])
@dp.async_task
async def cmd_ping_bot(message: types.Message):
    await message.delete()
    await message.answer("<b>🤙 На связи!</b>", parse_mode='HTML')



@dp.message_handler(IsOwner(), commands=['users'])
@dp.async_task
async def who_is_users(message: types.Message):
    pre_msg = config['ALLOWED_IDS']
    await message.delete()
    await message.answer(text=', '.join(pre_msg))



@dp.message_handler(IsOwner(), commands=['gitupdate'])
@dp.async_task
async def update_bot(message: types.Message):
    await message.delete()
    m = await message.answer('Выполняю команду...')
    run(['git', 'fetch'])
    run(['git', 'reset', '--hard', 'origin/main'])
    await m.edit_text('Бот обновлен, перезапуск...')
    # перезапуск программы
    await restart()





@dp.message_handler(IsOwner(), commands=['gitback'])
@dp.async_task
async def rollback_bot(message: types.Message):
    await message.delete()
    m = await message.answer('Выполняю команду...')
    run(['git', 'fetch'])
    run(['git', 'reset', '--hard', 'origin/main'])
    call(['git', 'reset', '--hard', 'HEAD~1'])
    await m.edit_text('Бот вернулся к предыдущей версии, перезапуск...')
    # перезапуск программы
    await restart()



@dp.message_handler(IsOwner(), commands=['log'])
@dp.async_task
async def sendlog(message: types.Message):
    await message.delete()
    with open(handler.baseFilename, 'rb') as file:
        await message.answer_document(file)



@dp.message_handler(IsOwner(), commands=['cleanlog'])
@dp.async_task
async def clean_log_file(message: types.Message):
    await message.delete()
    with open(handler.baseFilename, 'w') as log_file:
        log_file.write('')
    await message.answer('Файл логов успешно очищен!')



@dp.message_handler(IsOwner(), commands=['tokens'])
@dp.async_task
async def num_of_tokens(message: types.Message):
    await message.delete()
    await message.answer(f'Количество ключей OpenAI: {len(api)}')



@dp.message_handler(IsOwner(), commands=['addtokens'])
@dp.async_task
async def add_tokens(message: types.Message):
    text = message.text[10:]
    [config['OPENAI_TOKENS'].append(t) for t in [i.strip() for i in text.split(',')]]
    await confupdate()
    await message.answer('Новые токены добавлены!')


@dp.message_handler(IsOwner(), commands=['rtokens'])
@dp.async_task
async def remome_tokens(message: types.Message):
    text = message.text[7:]
    [config['OPENAI_TOKENS'].remove(t) for t in [i.strip() for i in text.split(',')]]
    await confupdate()
    await message.answer('Лишние токены удалены!')