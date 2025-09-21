from nicegui import ui, app

from lib.deca.hashes import hash32_func
from lib.model.animalType import AnimalType
from lib.model.constants import MEDALS
from lib.model.reserve import ReserveEnum


def andOrRadio(label):
    return ui.radio(['and', 'or'], value='and').props('inline').bind_value(app.storage.user, label)


def selectMulti(options, label):
    return ui.select(options=options, multiple=True, label=label, with_input=True, clearable=True).props('use-chips').bind_value(app.storage.user, label)


def footer():
    pass


def reservesOptions() -> dict:
    return {r.value: r.reserveName() for r in ReserveEnum}


def medalOptions() -> dict:
    return MEDALS


def animalsOptions() -> dict:
    return {hash32_func(a.name.lower()): a.animalName() for a in AnimalType}
