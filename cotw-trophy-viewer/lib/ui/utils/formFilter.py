from nicegui import ui

from lib.deca.hashes import hash32_func
from lib.model.animalType import AnimalType
from lib.model.constants import MEDALS
from lib.model.reserve import ReserveEnum


def andOrRadio():
    return ui.radio(['and', 'or'], value='and').props('inline')


def selectMulti(options, label):
    return ui.select(options=options, multiple=True, label=label, with_input=True, clearable=True).props('use-chips')


def footer():
    pass


def reservesOptions() -> dict:
    return {r.value: r.reserveName() for r in ReserveEnum}


def medalOptions() -> dict:
    return MEDALS


def animalsOptions() -> dict:
    return {hash32_func(a.name.lower()): a.animalName() for a in AnimalType}
