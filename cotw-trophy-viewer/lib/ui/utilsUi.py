from typing import List

from nicegui import ui

from lib.db.db import Db
from lib.model.animalType import AnimalType
from lib.model.constants import RESERVES, RATING_BADGES

def headerHome(db: Db):
    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            ui.label("TROPHIES").style("font-size:30px;color:#666;")
    with ui.row():
        dropdownFor(db.lodges(), "lodges")
        dropdownFor(reserves(), "reserves")
        dropdownFor(animals(), "animals")
        dropdownFor(badges(), "badges")
        ui.checkbox('show all animals')


def dropdownFor(options, label):
    (ui.select(options=options, multiple=True, label=label, with_input=True)
     .classes('w-50')
     .props('use-chips'))


def isDiamondTrophy(trophies, animal):
    for animalData in trophies.animals[animal]:
        if animalData.ratingIcon == 0:
            return True
    return False


def footer():
    pass


def reserves() -> List[str]:
    return [list(reserve_dict.keys())[0] for reserve_dict in RESERVES.values()]


def badges() -> List[str]:
    return list(set(RATING_BADGES.values()))


def animals() -> List[str]:
    return sorted([animal.animalName() for animal in AnimalType])
