import asyncio

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .bot import commands
from .bot.handlers import include_routers
from .bot.middlewares import register_middlewares
from .config import load_config
from .logger import setup_logger


async def on_shutdown(dispatcher: Dispatcher, bot: Bot, engine: AsyncEngine) -> None:
    """
    Shutdown event handler. This runs when the bot shuts down.
    """
    await commands.delete(bot)
    await dispatcher.storage.close()
    await bot.delete_webhook()
    await bot.session.close()
    await engine.dispose()


async def on_startup(bot: Bot, engine: AsyncEngine) -> None:
    """
    Startup event handler. This runs when the bot starts up.
    """
    async with engine.begin() as conn:
        from .db.models import Base
        await conn.run_sync(Base.metadata.create_all)
    await commands.setup(bot)


async def main() -> None:
    """
    Main function that initializes the bot and starts the event loop.
    """
    # Load config
    config = load_config()

    # Create async engine and sessionmaker
    engine = create_async_engine(
        url=config.database.url(),
        pool_pre_ping=True,
    )
    sessionmaker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    storage = RedisStorage.from_url(
        url=config.redis.dsn(),
    )
    bot = Bot(
        token=config.bot.TOKEN,
        parse_mode=ParseMode.HTML,
    )
    dp = Dispatcher(
        storage=storage,
        engine=engine,
        config=config,
        bot=bot,
    )

    # Register startup handler
    dp.startup.register(on_startup)
    # Register shutdown handler
    dp.shutdown.register(on_shutdown)

    # Include routes
    include_routers(dp)
    # Register middlewares
    register_middlewares(dp, config=config, redis=storage.redis, sessionmaker=sessionmaker)

    # Start the bot
    await bot.delete_webhook()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    # Set up logging
    setup_logger()
    # Run the bot
    asyncio.run(main())
