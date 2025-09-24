from nicegui import ui

from lib.model.animalType import AnimalType
from lib.model.constants import MEDALS
from lib.model.reserve import Reserve


def andOrRadio():
    return ui.radio(['and', 'or'], value='and').props('inline')


def selectMulti(options, label):
    return ui.select(options=options, multiple=True, label=label, with_input=True, clearable=True).props('use-chips')


def footer():
    pass


def reservesOptions() -> dict:
    return {r.value: r.reserveName() for r in Reserve}


def medalOptions() -> dict:
    return MEDALS


def animalsOptions() -> dict:
    return {a.value: a.animalName() for a in AnimalType}
