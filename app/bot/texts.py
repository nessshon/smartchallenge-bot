from abc import abstractmethod, ABCMeta

from aiogram.types import (
    InlineKeyboardButton,
    SwitchInlineQueryChosenChat,
    LoginUrl,
    WebAppInfo,
)
from aiogram.utils.markdown import hide_link


class Text(metaclass=ABCMeta):

    def __init__(self, language_code: str) -> None:
        self.language_code = language_code if language_code == "ru" else "en"

    @property
    @abstractmethod
    def data(self) -> dict:
        raise NotImplementedError

    def get(self, code: str) -> str:
        return self.data[self.language_code][code]


class TextMessage(Text):

    @property
    def data(self) -> dict:
        return {
            "ru": {
                "select_language": (
                    "👋 <b>Привет</b>, {full_name}!\n\n"
                    "Выберите язык:"
                ),
                "change_language": (
                    "<b>Выберите язык:</b>\n\n"
                ),
                "send_nickname": (
                    "<b>Отправьте свой псевдоним</b>,\n\n"
                    "который будет опубликован вместе с вашими результатами:"
                ),
                "send_github_username": (
                    "<b>Отправьте свою учетную запись GitHub</b>,\n\n"
                    "которую вы будете использовать для подачи заявок на участие в Smart Challenge. "
                    "Помните, возраст учетной записи должен быть не менее 1 месяца. (Формат: @username)"
                ),
                "send_codeforces_username": (
                    "<b>Отправьте свой дескриптор Codeforces</b>,\n\n"
                    "если он у вас есть. Иначе нажмите Пропустить."
                ),
                "main_menu": (
                        hide_link("https://telegra.ph//file/3ba499a5ad6e33f73527c.jpg") +
                        "🏆 <b>Добро пожаловать в TON Smart Challenge #5</b>\n\n"
                        "🚀 {full_name}, мы очень рады видеть вас на TON Smart Challenge!\n"
                        "🤖 Цель этого захватывающего конкурса - максимально раскрыть свои навыки.\n"
                        "💻 Готовы принять вызов и продемонстрировать свои навыки программирования?\n"
                ),
                "my_profile": (
                    "👤 <b>Мой профиль</b>\n\n"
                    "<b>Псевдоним:</b>\n"
                    "{nickname}\n"
                    "<b>Имя пользователя GitHub:</b>\n"
                    "{github_username}\n"
                    "<b>Имя пользователя Codeforces:</b>\n"
                    "{codeforces_username}\n"
                    "<b>Токен GitHub:</b>\n"
                    "{github_token}\n"
                    "<b>Адрес кошелька:</b>\n"
                    "{wallet_address}"
                ),
                "func_resources": (
                    "📙 <b>Ресурсы FunC</b>\n\n"
                    "Язык высокого уровня FunC используется для программирования смарт-контрактов в TON."
                ),
                "tact_resources": (
                    "📘 <b>Ресурсы Tact</b>\n\n"
                    "Tact — это новый язык программирования для смарт-контрактов блокчейна TON"
                    "он прост в использовании, имеет знакомый синтаксис и строгую систему типов,"
                    "газовый контроль и состав безнакладного типа,"
                    "что позволяет разработчикам писать сложные системы смарт-контрактов"
                    "с подтвержденными затратами на исполнение."
                )
            },
            "en": {
                "select_language": (
                    "👋 <b>Hello</b>, {full_name}!\n\n"
                    "Select language:"
                ),
                "change_language": (
                    "<b>Select language:</b>\n\n"
                ),
                "send_nickname": (
                    "<b>Send your nickname</b>,\n\n"
                    "that will be published along with your results:"
                ),
                "send_github_username": (
                    "<b>Send your GitHub account</b>\n\n"
                    "that you'll use for Smart Challenge submissions. "
                    "Remember, the account should be at least 1 month old. (Format: @username)"
                ),
                "send_codeforces_username": (
                    "<b>Send your Codeforces Handle</b>\n\n"
                    "if you have one. Else, press Skip."
                ),
                "main_menu": (
                        hide_link("https://telegra.ph//file/3ba499a5ad6e33f73527c.jpg") +
                        "🏆 <b>Welcome to TON Smart Challenge #5</b>\n\n"
                        "🚀 {full_name}, we're absolutely thrilled to have you on board for TON Smart Challenge!\n"
                        "🤖 This exciting contest is all about pushing your skills to the limit.\n"
                        "💻 Ready to jump into the challenge and showcase your coding skills?\n"
                ),
                "my_profile": (
                    "👤 <b>My profile</b>\n\n"
                    "<b>Nickname:</b>\n"
                    "{nickname}\n"
                    "<b>GitHub username:</b>\n"
                    "{github_username}\n"
                    "<b>Codeforces username:</b>\n"
                    "{codeforces_username}\n"
                    "<b>GitHub Token:</b>\n"
                    "{github_token}\n"
                    "<b>Wallet address:</b>\n"
                    "{wallet_address}"
                ),
                "func_resources": (
                    "📙 <b>FunC resources</b>\n\n"
                    "A high-level language FunC is used to program smart contracts on TON."
                ),
                "tact_resources": (
                    "📘 <b>Tact resources</b>\n\n"
                    "Tact is a new programming language for TON blockchain smart contracts "
                    "that is easy to use and has a familiar syntax, strong type system, "
                    "gas control, and zero-overhead type composition, "
                    "which enables developers to write complex smart contract systems "
                    "with verified execution costs."
                )
            }
        }


class TextButton(Text):

    @property
    def data(self) -> dict:
        return {
            "ru": {
                "back": "‹ Назад",
                "skip": "Пропустить ›",
                "my_profile": "👤 Мой профиль",
                "leaderboard": "🏆 Таблица лидеров",
                "func_resources": "📙 FunC ресурсы",
                "tact_resources": "📘 Tact ресурсы",

                "connect_wallet": "🟢 Подключить кошелек",
                "disconnect_wallet": "🔴 Отключить кошелек",
                "update_profile": "📝 Обновить профиль",
                "regenerate_github_token": "🔄 Сгенерировать токен GitHub",

                "tact_documentation": "📚 Документация Tact",
                "tact_examples": "🐾 Такт с примерами",
                "tact_community_chat": "👥 Чат разработчиков Tact",

                "func_documentation": "📚 Документация FunC",
                "func_cookbook": "👨‍🍳 Поваренная книга FunC",

                "ton_course": "💎 Курс TON Blockchain",
                "ton_dev_chat": "👥 Чат разработчиков TON",
            },
            "en": {
                "back": "‹ Back",
                "skip": "Skip ›",
                "my_profile": "👤 My profile",
                "leaderboard": "🏆 Leaderboard",
                "func_resources": "📙 FunC resources",
                "tact_resources": "📘 Tact resources",

                "connect_wallet": "🟢 Connect wallet",
                "disconnect_wallet": "🔴 Disconnect wallet",
                "update_profile": "📝 Update profile",
                "regenerate_github_token": "🔄 Generate GitHub token",

                "tact_documentation": "📚 Tact documentation",
                "tact_examples": "🐾 Tact by example",
                "tact_community_chat": "👥 Tact Developers chat",

                "func_documentation": "📚 FunC documentation",
                "func_cookbook": "👨‍🍳 FunC cookbook",

                "ton_course": "💎 TON Blockchain course",
                "ton_dev_chat": "👥 TON Developers chat",
            }
        }

    def get_button(
            self,
            code: str,
            url: str | None = None,
            web_app: WebAppInfo | None = None,
            login_url: LoginUrl | None = None,
            switch_inline_query: str | None = None,
            switch_inline_query_current_chat: str | None = None,
            switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat | None = None,
    ) -> InlineKeyboardButton:
        text = self.get(code)
        if url:
            return InlineKeyboardButton(text=text, url=url)
        elif web_app:
            return InlineKeyboardButton(text=text, web_app=web_app)
        elif login_url:
            return InlineKeyboardButton(text=text, login_url=login_url)
        elif switch_inline_query:
            return InlineKeyboardButton(text=text, switch_inline_query=switch_inline_query)
        elif switch_inline_query_current_chat:
            return InlineKeyboardButton(text=text, switch_inline_query_current_chat=switch_inline_query_current_chat)
        elif switch_inline_query_chosen_chat:
            return InlineKeyboardButton(text=text, switch_inline_query_chosen_chat=switch_inline_query_chosen_chat)
        return InlineKeyboardButton(text=text, callback_data=code)
