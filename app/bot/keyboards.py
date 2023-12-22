from aiogram.types import InlineKeyboardMarkup as Markup, WebAppInfo

from aiogram.types import InlineKeyboardButton as Button

from app.bot.texts import TextButton


def back(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("back")]
        ]
    )


def back_skip(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("back"),
             text_button.get_button("skip")],
        ]
    )


def main_menu(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("my_profile")],
            [text_button.get_button("func_resources")],
            [text_button.get_button("tact_resources")],
            [text_button.get_button("leaderboard",
                                    web_app=WebAppInfo(url="https://leaderboard.tonsmartchallenge.org/"))],
        ]
    )


def select_language(text_button: TextButton, include_back: bool = False) -> Markup:
    inline_keyboard = [
        [Button(text="🇷🇺 Русский", callback_data="ru"),
         Button(text="🇬🇧 English", callback_data="en")],
    ]
    if include_back:
        inline_keyboard.append([text_button.get_button("back")])
    return Markup(inline_keyboard=inline_keyboard)


def send_nickname(text_button: TextButton, username: str = None) -> Markup:
    if username:
        inline_keyboard = [
            [Button(text=username, callback_data=username)],
            [text_button.get_button("back")],
        ]
    else:
        inline_keyboard = [
            [text_button.get_button("back")]
        ]
    return Markup(inline_keyboard=inline_keyboard)


def my_profile(text_button: TextButton, wallet_is_connected: bool) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("update_profile")],
            [text_button.get_button("regenerate_github_token")],
            [text_button.get_button(
                "disconnect_wallet" if wallet_is_connected else "connect_wallet"
            )],
            [text_button.get_button("back")],
        ]
    )


def tact_resources(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("tact_documentation", url="https://docs.tact-lang.org/")],
            [text_button.get_button("tact_examples", url="https://tact-by-example.org/")],
            [text_button.get_button("tact_community_chat", url="https://t.me/tactlang")],
            [text_button.get_button("back")],
        ]
    )


def func_resources(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [text_button.get_button("func_documentation", url="https://docs.ton.org/develop/func/overview")],
            [text_button.get_button("func_cookbook", url="https://docs.ton.org/develop/func/cookbook")],
            [text_button.get_button("ton_course", "https://stepik.org/course/176754/info")],
            [text_button.get_button("ton_dev_chat",
                                    url=("https://t.me/tondev"
                                         if text_button.language_code == "ru" else
                                         "https://t.me/tondev_eng"))],
            [text_button.get_button("back")],
        ]
    )
