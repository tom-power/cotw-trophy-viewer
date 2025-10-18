
from nicegui import ui

from lib.db.db import Db
from lib.model.animal_type import AnimalType
from lib.model.animal_type_name import animalName
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.ui.components.icon_ui import IconUi
from lib.ui.components.filter_preset_ui import PresetUi
from lib.ui.utils.queries import Queries


class FilterButtonsUi:
    def __init__(self, update_grid_callback, clear_filter_callback):
        self.update_grid_callback = update_grid_callback
        self.clear_filter_callback = clear_filter_callback
        self._build_ui()

    def _build_ui(self):
        ui.button(text='APPLY', on_click=self.update_grid_callback)
        ui.button(text='CLEAR', on_click=self.clear_filter_callback)

