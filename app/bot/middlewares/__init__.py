from aiogram import Dispatcher
from aiogram_tonconnect.middleware import AiogramTonConnectMiddleware
from aiogram_tonconnect.tonconnect.storage.base import ATCRedisStorage
from aiogram_tonconnect.utils.qrcode import QRUrlProvider

from .config import ConfigMiddleware
from .database import DBSessionMiddleware
from .manager import ManagerMiddleware
from .throttling import ThrottlingMiddleware


def register_middlewares(dp: Dispatcher, **kwargs) -> None:
    """
    Register bot middlewares.
    """
    dp.update.outer_middleware.register(
        AiogramTonConnectMiddleware(
            storage=ATCRedisStorage(kwargs["redis"]),
            manifest_url=kwargs["config"].tonconnect.MANIFEST_URL,
            qrcode_provider=QRUrlProvider()
        )
    )
    dp.update.outer_middleware.register(DBSessionMiddleware(kwargs["sessionmaker"]))
    dp.update.outer_middleware.register(ConfigMiddleware(kwargs["config"]))
    dp.update.outer_middleware.register(ThrottlingMiddleware())
    dp.update.outer_middleware.register(ManagerMiddleware())


__all__ = [
    "register_middlewares",
]
