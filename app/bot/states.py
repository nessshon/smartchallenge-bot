from aiogram.fsm.state import StatesGroup

from aiogram.fsm.state import State as BaseState


class State(StatesGroup):
    select_language = BaseState()
    change_language = BaseState()

    send_nickname = BaseState()
    edit_nickname = BaseState()

    send_github_username = BaseState()
    edit_github_username = BaseState()

    send_codeforces_username = BaseState()
    edit_codeforces_username = BaseState()

    main_menu = BaseState()
    my_profile = BaseState()
    tact_resources = BaseState()
    func_resources = BaseState()
