from nicegui import ui

from lib.model.animalType import AnimalType
from lib.model.constants import RATING_BADGES
from lib.model.reserve import ReserveEnum

def uiFormFilter(db, queries):
    ui.space()
    dropdown(db.lodges(), "lodge", queries.updateQueryFor('lodges'))

    andOr(queries.updateQueryFor('reservesAndOr'))
    dropdown(reservesOptions(), "reserve", queries.updateQueryFor('reserves'))

    andOr(queries.updateQueryFor('badgesAndOr'))
    dropdown(badgeOptions(), "badge", queries.updateQueryFor('badge'))

    andOr(queries.updateQueryFor('animalsAndOr'))
    dropdown({0: "ALL"} | animalsOptions(), "animal", queries.updateQueryFor('animals'))

def andOr(callBack):
    ui.radio(['and', 'or'], value='or', on_change=callBack).props('inline')


def dropdown(options, label, callBack):
    ui.select(options=options, multiple=True, label=label, with_input=True, on_change=callBack).props('use-chips')


def checkbox(label, callback):
    ui.checkbox(text=label, value=False, on_change=callback)


def footer():
    pass


def reservesOptions() -> dict:
    return {r.value: r.reserveName() for r in ReserveEnum}


def badgeOptions() -> dict:
    return RATING_BADGES


def animalsOptions() -> dict:
    return {a.value: a.animalName() for a in AnimalType}
