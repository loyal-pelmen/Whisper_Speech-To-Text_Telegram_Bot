from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
import config


class IsOwner(BoundFilter):
    """
    Пользовательский фильтр "is_owner".
    """

    async def check(self, message: Message) -> bool:
        if config.OWNERS_IDS:
            return message.from_user.id in config.OWNERS_IDS or message.sender_chat.id in config.OWNERS_IDS
        elif 1 in config.OWNERS_IDS:
            return True
        else:
            return False


class IsUser(BoundFilter):
    """
    Фильтр, проверяющий разрешено ли пользователю пользоваться ботом
    """


    async def check(self, message: Message) -> bool:
        if config.ALLOWED_IDS:
            return message.from_user.id in config.ALLOWED_IDS or message.from_user.id in config.OWNERS_IDS or message.sender_chat.id in config.ALLOWED_IDS or 1 in config.OWNERS_IDS or message.sender_chat.id in config.OWNERS_IDS
        elif 1 in config.ALLOWED_IDS:
            return True
        else:
            return False