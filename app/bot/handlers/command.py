from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.handlers.windows import Window
from app.bot.manager import Manager

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command("start"))
async def start_command(message: Message, manager: Manager) -> None:
    if manager.user_db.wallet_address:
        await Window.main_menu(manager)
    else:
        await Window.select_language(manager)

    await manager.delete_message(message)


@router.message(Command("language"))
async def language_command(message: Message, manager: Manager) -> None:
    if manager.user_db.wallet_address:
        await Window.change_language(manager)
    else:
        await Window.select_language(manager)

    await manager.delete_message(message)
