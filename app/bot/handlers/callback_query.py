import uuid
from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_tonconnect import ATCManager
from aiogram_tonconnect.tonconnect.models import ConnectWalletCallbacks

from app.bot.handlers.windows import Window
from app.bot.manager import Manager
from app.bot.states import State
from app.bot.utils import raw_to_userfriendly
from app.db.models import UserDB

router = Router()
router.callback_query.filter(F.message.chat.type == "private")


@router.callback_query(State.select_language)
async def select_language_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data in ["ru", "en"]:
        callbacks = ConnectWalletCallbacks(
            before_callback=Window.select_language,
            after_callback=Window.send_nickname,
        )
        await UserDB.update(
            manager.async_session,
            manager.user.id,
            language_code=call.data,
        )
        await atc_manager.update_interfaces_language(call.data)
        await atc_manager.open_connect_wallet_window(callbacks)

    await call.answer()


@router.callback_query(State.change_language)
async def change_language_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data == "back":
        await Window.main_menu(manager)

    elif call.data in ["ru", "en"]:
        manager.user_db = await UserDB.update(
            manager.async_session,
            manager.user.id,
            language_code=call.data,
        )
        manager.text_button.language_code = call.data
        manager.text_message.language_code = call.data
        await atc_manager.update_interfaces_language(call.data)
        await Window.main_menu(manager)

    await call.answer()


@router.callback_query(State.send_nickname)
async def send_nickname_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data == "back":
        callbacks = ConnectWalletCallbacks(
            before_callback=Window.select_language,
            after_callback=Window.send_nickname,
        )
        await atc_manager.open_connect_wallet_window(callbacks)
    else:
        await manager.state.update_data(nickname=call.data)
        await Window.send_github_username(manager)

    await call.answer()


@router.callback_query(State.edit_nickname)
async def edit_nickname_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "back":
        await Window.my_profile(manager)
    else:
        await manager.state.update_data(nickname=call.data)
        manager.user_db = await UserDB.update(
            manager.async_session,
            manager.user.id,
            nickname=call.data,
        )
        await Window.send_github_username(manager)

    await call.answer()


@router.callback_query(State.send_github_username)
async def send_github_username_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "back":
        await Window.send_nickname(manager)

    await call.answer()


@router.callback_query(State.edit_github_username)
async def send_github_username_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "back":
        await Window.send_nickname(manager)
        await manager.state.set_state(State.edit_nickname)

    await call.answer()


@router.callback_query(State.send_codeforces_username)
async def send_codeforces_username_callback_query(call: CallbackQuery, manager: Manager,
                                                  atc_manager: ATCManager) -> None:
    if call.data == "back":
        await Window.send_github_username(manager)

    elif call.data == "skip":
        await manager.state.update_data(codeforces_username=None)
        state_data = await manager.state.get_data()
        await UserDB.update(
            manager.async_session,
            manager.user.id,
            nickname=state_data.get("nickname"),
            github_username=state_data.get("github_username"),
            codeforces_username=state_data.get("codeforces_username"),
            github_token=str(uuid.uuid4()),
            wallet_address=raw_to_userfriendly(atc_manager.user.account_wallet.address),
        )
        await Window.main_menu(manager)

    await call.answer()


@router.callback_query(State.edit_codeforces_username)
async def edit_codeforces_username_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "back":
        await Window.send_github_username(manager)
        await manager.state.set_state(State.edit_github_username)

    elif call.data == "skip":
        await manager.state.update_data(codeforces_username=None)
        manager.user_db = await UserDB.update(
            manager.async_session,
            manager.user.id,
            codeforces_username=None,
        )
        await Window.my_profile(manager)

    await call.answer()


@router.callback_query(State.main_menu)
async def main_menu_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "my_profile":
        await Window.my_profile(manager)

    elif call.data == "func_resources":
        await Window.func_resources(manager)

    elif call.data == "tact_resources":
        await Window.tact_resources(manager)

    await call.answer()


@router.callback_query(State.func_resources)
@router.callback_query(State.tact_resources)
async def resources_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if call.data == "back":
        await Window.main_menu(manager)

    await call.answer()


@router.callback_query(State.my_profile)
async def my_profile_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data == "back":
        await Window.main_menu(manager)

    elif call.data == "update_profile":
        await Window.send_nickname(manager)
        await manager.state.set_state(State.edit_nickname)

    elif call.data == "regenerate_github_token":
        manager.user_db = await UserDB.update(
            manager.async_session,
            manager.user.id,
            github_token=str(uuid.uuid4()),
        )
        await Window.my_profile(manager)

    elif call.data == "disconnect_wallet":
        if atc_manager.tonconnect.connected:
            with suppress(Exception):
                await atc_manager.tonconnect.disconnect()
        manager.user_db = await UserDB.update(
            manager.async_session,
            manager.user.id,
            wallet_address=None,
        )
        await manager.state.update_data(account_wallet=None)
        await Window.my_profile(manager)

    elif call.data == "connect_wallet":
        callbacks = ConnectWalletCallbacks(
            before_callback=Window.my_profile,
            after_callback=Window.my_profile,
        )
        await atc_manager.open_connect_wallet_window(callbacks)

    await call.answer()
