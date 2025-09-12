from nicegui import ui

from lib.model.animalType import AnimalType
from lib.model.constants import RATING_BADGES
from lib.model.reserve import ReserveEnum

def formFilterButton(param):
    ui.button(text='FILTER', on_click=param)
