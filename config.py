from ujson import load

with open('./config.json', 'r') as config_file:
    config = load(config_file)


BOT_TOKEN = str(config['BOT_TOKEN'])
LOG_BOT_TOKEN = str(config['LOG_BOT_TOKEN']) 
ALLOWED_IDS = list(config['ALLOWED_IDS'])
OWNERS_IDS = list(config['OWNERS_IDS'])

WEBHOOK = str(eval(config['WEBHOOK']))if str(config['WEBHOOK']) != 'False' else ''
WEBHOOK_HOST = str(config['WEBHOOK_HOST'])
WEBAPP_HOST = str(config['WEBAPP_HOST'])
WEBAPP_PORT = int(config['WEBAPP_PORT'])
UPDATESPENDING = eval(config['UPDATESPENDING'])
MAXCONNECTIONS = int(config['MAXCONNECTIONS'])

OPENAI_TOKENS = list(config['OPENAI_TOKENS'])

LOG_LEVEL = str(config['LOG_LEVEL'])
