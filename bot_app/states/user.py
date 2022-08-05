from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    main = State()

    class NewInformation(StatesGroup):
        full_name = State()
        gender = State()
        birthday = State()
        hight = State()
        mass = State()
        shoes_size = State()
        clothet_size = State()

    class NewQuestion(StatesGroup):
        text = State()