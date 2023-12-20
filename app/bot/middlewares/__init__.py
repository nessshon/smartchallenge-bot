from aiogram import Dispatcher
from aiogram_tonconnect.middleware import AiogramTonConnectMiddleware

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
            redis=kwargs["redis"],
            manifest_url=kwargs["config"].tonconnect.MANIFEST_URL,
            exclude_wallets=["mytonwallet"],  # noqa
        )
    )
    dp.update.outer_middleware.register(DBSessionMiddleware(kwargs["sessionmaker"]))
    dp.update.outer_middleware.register(ConfigMiddleware(kwargs["config"]))
    dp.update.outer_middleware.register(ThrottlingMiddleware())
    dp.update.outer_middleware.register(ManagerMiddleware())


__all__ = [
    "register_middlewares",
]
