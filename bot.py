from aiogram.utils.executor import start_webhook, start_polling
from dispatcher import dp, start, stop, WEBHOOK_PATH
from config import WEBAPP_HOST, WEBAPP_PORT, WEBHOOK
import handlers


if __name__ == "__main__":
    if WEBHOOK:
        start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=start,
        on_shutdown=stop,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT)
    else:
        start_polling(dp, skip_updates=True, on_startup=start, on_shutdown=stop)  # Не пропускайте обновления, если ваш бот будет обрабатывать платежи или другие важные вещи.