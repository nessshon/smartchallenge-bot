from aiogram.utils.markdown import hbold, hcode
from aiogram_tonconnect.tonconnect.models import AccountWallet

from app.bot import keyboards
from app.bot.manager import Manager
from app.bot.states import State
from app.bot.utils import raw_to_userfriendly
from app.db.models import UserDB


class Window:

    @staticmethod
    async def select_language(manager: Manager, **_) -> None:
        text = manager.text_message.get("select_language")
        reply_markup = keyboards.select_language(manager.text_button)

        frmt_data = {"full_name": hbold(manager.user.full_name)}

        await manager.send_message(text.format_map(frmt_data), reply_markup=reply_markup)
        await manager.state.set_state(State.select_language)

    @staticmethod
    async def change_language(manager: Manager) -> None:
        text = manager.text_message.get("change_language")
        reply_markup = keyboards.select_language(manager.text_button, include_back=True)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.change_language)

    @staticmethod
    async def send_nickname(manager: Manager, **_) -> None:
        text = manager.text_message.get("send_nickname")
        reply_markup = keyboards.send_nickname(manager.text_button, username=manager.user.username)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.send_nickname)

    @staticmethod
    async def send_github_username(manager: Manager) -> None:
        text = manager.text_message.get("send_github_username")
        reply_markup = keyboards.back(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.send_github_username)

    @staticmethod
    async def send_codeforces_username(manager: Manager) -> None:
        text = manager.text_message.get("send_codeforces_username")
        reply_markup = keyboards.back_skip(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.send_codeforces_username)

    @staticmethod
    async def main_menu(manager: Manager) -> None:
        text = manager.text_message.get("main_menu")
        reply_markup = keyboards.main_menu(manager.text_button)

        frmt_data = {"full_name": hbold(manager.user.full_name)}

        await manager.send_message(text.format_map(frmt_data), reply_markup=reply_markup)
        await manager.state.set_state(State.main_menu)

    @staticmethod
    async def func_resources(manager: Manager) -> None:
        text = manager.text_message.get("func_resources")
        reply_markup = keyboards.func_resources(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.func_resources)

    @staticmethod
    async def tact_resources(manager: Manager) -> None:
        text = manager.text_message.get("tact_resources")
        reply_markup = keyboards.tact_resources(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup)
        await manager.state.set_state(State.tact_resources)

    @staticmethod
    async def my_profile(manager: Manager, account_wallet: AccountWallet = None, **_) -> None:
        if account_wallet:
            manager.user_db = await UserDB.update(
                manager.async_session,
                manager.user.id,
                wallet_address=raw_to_userfriendly(account_wallet.address),
            )

        text = manager.text_message.get("my_profile")
        reply_markup = keyboards.my_profile(manager.text_button, manager.user_db.wallet_address is not None)

        frmt_data = {
            "nickname": hcode(manager.user_db.nickname),
            "github_token": hcode(manager.user_db.github_token),
            "github_username": hcode(manager.user_db.github_username),
            "codeforces_username": "-" if not manager.user_db.codeforces_username else hcode(
                manager.user_db.codeforces_username),
            "wallet_address": "-" if not manager.user_db.wallet_address else hcode(
                manager.user_db.wallet_address),
        }

        await manager.send_message(text.format_map(frmt_data), reply_markup=reply_markup)
        await manager.state.set_state(State.my_profile)
