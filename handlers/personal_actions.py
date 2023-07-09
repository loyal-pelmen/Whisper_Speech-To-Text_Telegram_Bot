from aiogram import types
from dispatcher import dp, handler
from config import config
from filters import IsOwner
from subprocess import call, run
from utils.my_utils import restart, confupdate



api = config['OPENAI_TOKENS']


@dp.message_handler(IsOwner(), commands='help')
@dp.async_task
async def help(msg: types.Message):
    await msg.delete()
    await msg.answer(f'''
<b>Запишите голосовое или видеосообщение и бот пришлёт расшифровку.</b>
    
<b>Функции для Админов:</b>

/restart - перезапуск бота.
/gitupdate - обновляет бота до последней версии.
/gitback - возвращает версию на n версий назад от последней.
/log - отправляет файл с логами.
/cleanlog - очищает файл с логами.
/changelogbot - добавляет или изменяет ключ для бота с логами.
/rlogbot - удаляет бота с логами.
/ping - проверка доступности бота.
/users - отправляет список пользователей.
/addusers - добавляет пользователей.
/rusers - удаляет пользователей.
/admins - отправляет список админов.
/addadmins - добавляет админов.
/radmins - удаляет админов.
/tokens - отправляет количество токенов.
/printtokens - отправляет список токенов.
/addtokens - добавляет токены.
/rtokens - удаляет токены.''', parse_mode='HTML')



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
    await message.delete()
    pre_msg = config['ALLOWED_IDS']

    if not(1 in pre_msg):
        if pre_msg:
            await message.answer(text=str(pre_msg)[1:-1])
        else:
            await message.answer(text='У вас нет пользователей.')
    else:
        await message.answer(text='У вас каждый - пользователь👏.')



@dp.message_handler(IsOwner(), commands=['admins'])
@dp.async_task
async def who_is_admin(message: types.Message):
    await message.delete()
    pre_msg = config['OWNERS_IDS']

    if not (1 in pre_msg):
        if pre_msg:
            await message.answer(text=str(pre_msg)[1:-1])
        else:
            await message.answer(text='У вас нет админов.')
    else:
        await message.answer(text='У вас каждый - админ😎👏.')



@dp.message_handler(IsOwner(), commands=['addusers'])
@dp.async_task
async def add_users(message: types.Message):
    try:
        await message.delete()
        text = (message.text[9:]).strip()
        one = not (',' in text)
        if text:
            if one:
                text = int(text.strip())
                config['ALLOWED_IDS'].append(text)
            else:
                users = list(map(str.strip, text.split(',')))
                new_users = [int(user) for user in users[::-1] if (user not in config['ALLOWED_IDS']) and user.isdigit()]
                config['ALLOWED_IDS'].extend(new_users)

            await confupdate()
            await message.answer('Новые пользователи добавлены!')
        else:
            await message.answer('Для того, чтобы воспользоваться этой функцией, сделайте отступ и добавьте id пользователей через запятую.')
    except:
        await message.answer('Что-то не так... Проверьте что написали и повторите попытку.')



@dp.message_handler(IsOwner(), commands=['addadmins'])
@dp.async_task
async def add_admins(message: types.Message):
    try:
        await message.delete()
        text = (message.text[10:]).strip()
        one = not (',' in text)
        if text:
            if one:
                text = text.strip()
                if text.isdigit():
                    config['OWNERS_IDS'].append(int(text))
                else:
                    exit()
            else:
                admins = list(map(str.strip, text.split(',')))
                new_users = [int(admin) for admin in admins[::-1] if (admin not in config['OWNERS_IDS']) and admin.isdigit()]
                config['OWNERS_IDS'].extend(new_users)

            await confupdate()
            await message.answer('Новые админы добавлены!')
        else:
            await message.answer('Для того, чтобы воспользоваться этой функцией, сделайте отступ и добавьте id админов через запятую.')
    except:
        await message.answer('Что-то не так... Проверьте что написали и повторите попытку.')



@dp.message_handler(IsOwner(), commands=['radmins'])
@dp.async_task
async def remome_admins(message: types.Message):
    try:
        await message.delete()
        text = (message.text[8:]).strip()
        one = not (',' in text)

        if text:
            if one:
                if text.isdigit():
                    config['OWNERS_IDS'].remove(int(text))
                else:
                    exit()
            else:
                [config['OWNERS_IDS'].remove(user) for user in[int(id.strip()) for id in text.split(',') if id.strip().isdigit()] if user in config['OWNERS_IDS']]


            await confupdate()
            await message.answer('Лишние id удалены!')
        else:
            await message.answer('Для того, чтобы воспользоваться этой функцией, сделайте отступ и добавьте id через запятую.')
    except:
        await message.answer('Что-то не так... Проверьте что написали и повторите попытку.')



@dp.message_handler(IsOwner(), commands=['rusers'])
@dp.async_task
async def remome_users(message: types.Message):
    try:
        await message.delete()
        text = (message.text[7:]).strip()
        one = not (',' in text)

        if text:
            if one:
                text = text.strip()
                if text.isdigit():
                    config['ALLOWED_IDS'].remove(int(text))
                else:
                    exit()
            else:
                [config['ALLOWED_IDS'].remove(user) for user in[int(id.strip()) for id in text.split(',') if id.strip().isdigit()] if user in config['ALLOWED_IDS']]


            await confupdate()
            await message.answer('Лишние id удалены!')
        else:
            await message.answer('Для того, чтобы воспользоваться этой функцией, сделайте отступ и добавьте id через запятую.')
    except:
        await message.answer('Что-то не так... Проверьте что написали и повторите попытку.')



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
    text = ((message.text)[8:]).strip()

    if not text:
        await message.answer('Чтобы использовать эту команду, сделайте отступ от /gitback и укажите, на сколко версий назад вы хотите вернуться. Будьте осторожны! Откат на некоторые версии могут привести к неработоспособности бота.')
    else:
        if text.isdigit():
            m = await message.answer('Выполняю команду...')
            run(['git', 'fetch'])
            run(['git', 'reset', '--hard', 'origin/main'])
            call(['git', 'reset', '--hard', f'HEAD~{text}'])
            await m.edit_text('Бот вернулся к предыдущей версии, перезапуск...')
            # перезапуск программы
            await restart()
        else:
            await message.answer('Что-то не так... Проверьте что написали и повторите попытку.')



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



@dp.message_handler(IsOwner(), commands=['printtokens'])
@dp.async_task
async def print_tokens(message: types.Message):
    await message.delete()
    await message.answer(text=', '.join(api))



@dp.message_handler(IsOwner(), commands=['addtokens'])
@dp.async_task
async def add_tokens(message: types.Message):
    await message.delete()
    text = (message.text[10:]).strip()
    one = not (',' in text)
    if text:
        if one:
            text = text.strip()
            config['OPENAI_TOKENS'].append(text)
        else:
            tokens = list(map(str.strip, text.split(',')))
            new_tokens = [token for token in tokens[::-1] if (token not in config['OPENAI_TOKENS']) and (token != '')]
            config['OPENAI_TOKENS'].extend(new_tokens)

        await confupdate()
        await message.answer('Новые токены добавлены!')
    else:
        await message.answer('Для того, чтобы воспользоваться этой функцией, сделайте отступ и добавьте токены через запятую.')


@dp.message_handler(IsOwner(), commands=['rtokens'])
@dp.async_task
async def remome_tokens(message: types.Message):
    await message.delete()
    text = (message.text[8:]).strip()
    one = not (',' in text)

    if text:
        if one:
            text = text.strip()
            config['OPENAI_TOKENS'].remove(text)
        else:
            for token in text.split(','):
                token = token.strip()
                if token in config['OPENAI_TOKENS'] and token != '':
                    config['OPENAI_TOKENS'].remove(token)

        await confupdate()
        await message.answer('Лишние токены удалены!')
    else:
        await message.answer('Для того, чтобы воспользоваться этой функцией, сделайте отступ и добавьте токены через запятую.')


@dp.message_handler(IsOwner(), commands=['changelogbot'])
@dp.async_task
async def change_log_bot(message: types.Message):
    try:
        await message.delete()
        text = (message.text[13:]).strip()
        one = not (',' in text)

        if text:
            if one:
                text = text.strip()
                config['LOG_BOT_TOKEN'] = text
                await confupdate()
                await message.answer('Токен успешно изменён!')
            else:
                await message.answer('Что-то не так... Проверьте что написали и повторите попытку.')

            
        else:
            await message.answer('Для того, чтобы воспользоваться этой функцией, сделайте отступ и добавьте ключ для телеграм бота.')
    except:
        await message.answer('Что-то не так... Проверьте что написали и повторите попытку.')



@dp.message_handler(IsOwner(), commands=['rlogbot'])
@dp.async_task
async def remove_log_bot(message: types.Message):
    await message.delete()
    config['LOG_BOT_TOKEN'] = ""
    await confupdate()
    await message.answer('Ключ для бота с логами удалён.')
