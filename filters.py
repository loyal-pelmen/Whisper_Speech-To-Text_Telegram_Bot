from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import BoundFilter
import config


class IsOwner(BoundFilter):
    """
    Пользовательский фильтр "is_owner".
    """

    async def check(self, message: Message) -> bool:
        return message.from_user.id in config.OWNERS_IDS


class IsUser(BoundFilter):
    """
    Фильтр, проверяющий разрешено ли пользователю пользоваться ботом
    """


    async def check(self, message: Message) -> bool:
        return message.from_user.id in config.ALLOWED_IDS or message.from_user.id in config.OWNERS_IDS