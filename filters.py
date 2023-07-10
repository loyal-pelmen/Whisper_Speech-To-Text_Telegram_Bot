from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
import config


class IsOwner(BoundFilter):
    """
    Фильтр, проверяющий имеет ли пользователь админские права.
    """

    async def check(self, message: Message) -> bool:
        if config.OWNERS_IDS:
            return message.from_id in config.OWNERS_IDS or message.from_id in config.OWNERS_IDS or 1 in config.OWNERS_IDS
        else:
            return False


class IsUser(BoundFilter):
    """
    Фильтр, проверяющий разрешено ли пользователю пользоваться ботом.
    """


    async def check(self, message: Message) -> bool:
        if config.ALLOWED_IDS or config.ALLOWED_GROUPS_IDS or config.OWNERS_IDS:
            return message.from_id in config.ALLOWED_IDS or message.from_id in config.OWNERS_IDS or 1 in config.OWNERS_IDS or message.from_id in config.OWNERS_IDS or message.chat.id in config.ALLOWED_GROUPS_IDS or message.chat.id in config.ALLOWED_GROUPS_IDS or 1 in config.ALLOWED_GROUPS_IDS
        else:
            return False