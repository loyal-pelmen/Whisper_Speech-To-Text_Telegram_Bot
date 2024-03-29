from ujson import load

with open('./config.json', 'r') as config_file:
    config = load(config_file)

PROXY = str(config['PROXY'])
BOT_TOKEN = str(config['BOT_TOKEN'])
LOG_BOT_TOKEN = str(config['LOG_BOT_TOKEN']) 
ALLOWED_IDS = list(config['ALLOWED_IDS'])
OWNERS_IDS = list(config['OWNERS_IDS'])
ALLOWED_GROUPS_IDS = list(config['ALLOWED_GROUPS_IDS'])

WEBHOOK = bool(config['WEBHOOK'])
WEBHOOK_HOST = str(config['WEBHOOK_HOST'])
WEBAPP_HOST = str(config['WEBAPP_HOST'])
WEBAPP_PORT = int(config['WEBAPP_PORT'])
UPDATESPENDING = bool(config['UPDATESPENDING'])
MAXCONNECTIONS = int(config['MAXCONNECTIONS'])

OPENAI_TOKENS = list(config['OPENAI_TOKENS'])

LOG_LEVEL = str(config['LOG_LEVEL']).upper()
