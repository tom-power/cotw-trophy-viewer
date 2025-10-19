from typing import Any

from nicegui import ui
from nicegui.testing import User


def get_presets_select_value(user: User) -> int | None:
    return _get_select_value(user, ['layton lake lodge todo'])

def get_lodge_select_value(user: User) -> int | None:
    return _get_select_value(user, ['LAYTON LAKE #1'])

def get_medal_select_value(user: User) -> int | None:
    return _get_select_value(user, ['DIAMOND'])

def _get_select_value(user: User, values) -> int | None:
    select = None
    all_selects = user.find(ui.select).elements
    for select in all_selects:
        if hasattr(select, 'options') and isinstance(select.options, dict):
            if any(str(v).upper() in values for v in select.options.values()):
                select = select
                break

    if select is not None and select.value is not None and len(select.value) > 0:
        return select.value[0]
    return None

def get_all_animals_checkbox_value(user: User) -> bool:
    checkbox__elements = user.find(ui.checkbox).elements
    return list(filter(lambda e: e.text == 'Include all animals', checkbox__elements))[0].value