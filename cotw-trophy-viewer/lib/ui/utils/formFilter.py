from nicegui import ui

from lib.deca.hashes import hash32_func
from lib.model.animalType import AnimalType
from lib.model.constants import RATING_BADGES
from lib.model.reserve import ReserveEnum


def andOrRadio(callBack):
    ui.radio(['and', 'or'], value='and', on_change=callBack).props('inline')


def select(options, label, callBack):
    return ui.select(options=options, multiple=True, label=label, with_input=True, clearable=True, on_change=callBack).props('use-chips')


def checkbox(label, callback):
    ui.checkbox(text=label, value=False, on_change=callback)


def footer():
    pass


def reservesOptions() -> dict:
    return {r.value: r.reserveName() for r in ReserveEnum}


def badgeOptions() -> dict:
    return RATING_BADGES


def animalsOptions() -> dict:
    return {hash32_func(a.name.lower()): a.animalName() for a in AnimalType}
