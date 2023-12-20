from aiogram import Dispatcher
from aiogram_tonconnect.handlers import AiogramTonConnectHandlers

from . import callback_query
from . import command
from . import error
from . import message


def include_routers(dp: Dispatcher) -> None:
    """
    Include bot routers.
    """

    AiogramTonConnectHandlers().register(dp)

    dp.include_routers(
        *[
            error.router,
            command.router,
            message.router,
            callback_query.router,
        ]
    )


__all__ = [
    "include_routers",
]
