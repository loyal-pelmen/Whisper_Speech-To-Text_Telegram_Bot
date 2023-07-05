from dotenv import load_dotenv


BOT_TOKEN = str(load_dotenv('BOT_TOKEN'))   #Получаем токен бота из env
LOG_BOT_TOKEN = (str(load_dotenv('LOG_BOT_TOKEN')) if str(load_dotenv('LOG_BOT_TOKEN')) != '' else print('Токена для логов не обнаружено'))   #Получаем токен бота для логов из env (если пустой, то не будет отправки)
ALLOWED_IDS = list(map(int, list(map(str.strip, str(load_dotenv('ALLOWED_IDS')).split(',')))))    #получаем строку из env, делим на список строк, позже преобразуем до списка с int
OWNERS_IDS = list(map(int, list(map(str.strip, str(load_dotenv('OWNERS_IDS')).split(',')))))

WEBHOOK = bool(load_dotenv('WEBHOOK') if load_dotenv('WEBHOOK') == 'True' else '')
WEBHOOK_HOST = str(load_dotenv('WEBHOOK_HOST'))
WEBAPP_HOST = str(load_dotenv('WEBAPP_HOST'))
WEBAPP_PORT = int(load_dotenv('WEBAPP_PORT'))
UPDATESPENDING = bool(load_dotenv('UPDATESPENDING') if load_dotenv('UPDATESPENDING') == 'True' else '')
MAXCONNECTIONS = int(load_dotenv('MAXCONNECTIONS'))

OPENAI_TOKENS = (list(map(str.strip, str(load_dotenv('OPENAI_TOKENS')).split(','))) if list(map(str.strip, str(load_dotenv('OPENAI_TOKENS')).split(','))) else exit('У вас нет токенов Openai'))

