from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    main = State()

    class MassSend(StatesGroup):
        to_all_message = State()
