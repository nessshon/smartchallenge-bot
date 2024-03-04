import uuid

from aiogram import Router, F
from aiogram.types import Message
from aiogram_tonconnect import ATCManager

from app.bot.handlers.windows import Window
from app.bot.manager import Manager
from app.bot.states import State
from app.db.models import UserDB

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(State.send_nickname)
@router.message(State.edit_nickname)
async def send_nickname_message(message: Message, manager: Manager) -> None:
    if message.content_type == "text" and len(message.text) <= 64:
        await manager.state.update_data(nickname=message.text)
        current_state = await manager.state.get_state()

        if current_state == State.edit_nickname.state:
            manager.user_db = await UserDB.update(
                manager.async_session,
                manager.user.id,
                nickname=message.text,
            )
            await Window.send_github_username(manager)
            await manager.state.set_state(State.edit_github_username)
        else:
            await Window.send_github_username(manager)

    await manager.delete_message(message)


@router.message(State.send_github_username)
@router.message(State.edit_github_username)
async def send_github_username_message(message: Message, manager: Manager) -> None:
    if message.content_type == "text" and len(message.text) <= 64:
        await manager.state.update_data(github_username=message.text)
        current_state = await manager.state.get_state()

        if current_state == State.edit_github_username.state:
            manager.user_db = await UserDB.update(
                manager.async_session,
                manager.user.id,
                github_username=message.text,
            )
            await Window.send_codeforces_username(manager)
            await manager.state.set_state(State.edit_codeforces_username)
        else:
            await Window.send_codeforces_username(manager)

    await manager.delete_message(message)


@router.message(State.send_codeforces_username)
@router.message(State.edit_codeforces_username)
async def send_codeforces_username_message(message: Message, manager: Manager, atc_manager: ATCManager) -> None:
    if message.content_type == "text" and len(message.text) <= 64:
        await manager.state.update_data(codeforces_username=message.text)
        current_state = await manager.state.get_state()

        if current_state == State.edit_codeforces_username.state:
            manager.user_db = await UserDB.update(
                manager.async_session,
                manager.user.id,
                codeforces_username=message.text,
            )
            await Window.my_profile(manager)
        else:
            state_data = await manager.state.get_data()
            await UserDB.update(
                manager.async_session,
                manager.user.id,
                nickname=state_data.get("nickname"),
                github_username=state_data.get("github_username"),
                codeforces_username=state_data.get("codeforces_username"),
                github_token=str(uuid.uuid4()),
                wallet_address=atc_manager.user.account_wallet.address.to_userfriendly(),
            )
            await Window.main_menu(manager)

    await manager.delete_message(message)


@router.message()
async def default_message(message: Message, manager: Manager) -> None:
    await manager.delete_message(message)
