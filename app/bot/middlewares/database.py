from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.models import UserDB


class DBSessionMiddleware(BaseMiddleware):
    """
    Middleware for handling database sessions.
    """

    def __init__(self, sessionmaker: async_sessionmaker):
        """
        Initialize the DBSessionMiddleware.

        :param sessionmaker: The async sessionmaker object for creating database sessions.
        """
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Call the middleware.

        :param handler: The handler function.
        :param event: The Telegram event.
        :param data: Additional data.
        """

        async with self.sessionmaker() as async_session:
            user: User = data.get("event_from_user")
            if user is not None:
                user_db = await UserDB.create_or_update(
                    async_session,
                    id=user.id,
                    full_name=user.full_name,
                    username=f"@{user.username}"
                )
                # Pass the user_db to the handler function
                data["user_db"] = user_db

        # Create a new session using the sessionmaker
        async with self.sessionmaker() as async_session:
            # Pass the async_session and sessionmaker to the handler function
            data["async_session"] = async_session
            data["sessionmaker"] = self.sessionmaker

            # Call the handler function with the event and data
            return await handler(event, data)
