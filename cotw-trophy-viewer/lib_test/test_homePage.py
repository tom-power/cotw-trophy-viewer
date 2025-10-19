from typing import Any

from nicegui import ui
from nicegui.testing import User


def get_presets_select_value(user: User) -> int | None:
    return _get_select_value(user, ['great one todo'])

def get_medal_select_value(user: User) -> int | None:
    return _get_select_value(user, ['DIAMOND'])

def _get_select_value(user: User, options) -> int | None:
    select = get_select(user, options)
    if select is not None and select.value is not None:
        if type(select.value) == int:
            return select.value
        if len(select.value) > 0:
            return select.value[0]
    return None

def get_select(user: User, options) -> Any | None:
    getSelect = None
    all_selects = user.find(ui.select).elements
    for select in all_selects:
        if hasattr(select, 'options') and isinstance(select.options, dict):
            if any(str(v).upper() in str(options).upper() for v in select.options.values()):
                getSelect = select
                break
    return getSelect

def get_all_animals_checkbox_value(user: User) -> bool:
    return get_all_animals_checkbox(user).value

def get_all_animals_checkbox(user: User):
    checkbox__elements = user.find(ui.checkbox).elements
    return list(filter(lambda e: e.text == 'Include all animals', checkbox__elements))[0]