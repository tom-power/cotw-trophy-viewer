from nicegui import ui

from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.ui.components.data_grid_ui import DataGridUi
from lib.ui.components.filter_ui import FilterUi
from lib.ui.components.lodge_file_ui import LodgeFileUi
from lib.ui.components.preset_ui import PresetUi
from lib.ui.components.theme_ui import ThemeUi
from lib.ui.utils.formFilter import footer
from lib.ui.utils.paths import Paths


class HomePage:

    def __init__(self, paths: Paths):
        self.paths = paths
        self.db = Db(self.paths.getLoadPath())

        self.filter_controller = None
        self.preset_controller = None
        self.grid_controller = None

        self._build_ui()

    def _build_ui(self):
        ThemeUi.apply_theme()

        with ui.grid(columns='800px 1fr 390px').classes('w-full gap-0'):
            self.filter_controller = FilterUi(self.db, self._updateGrid, self._clear)

            ui.space()

            with ui.card():
                LodgeFileUi(self.paths, self._reload)
                self.preset_controller = PresetUi(self.db, self.filter_controller, self._updateGrid)

        self.grid_controller = DataGridUi(self.db, self.filter_controller)

        footer()

    def _clear(self):
        self.filter_controller.clear_form()
        self.preset_controller.selectPresets.set_value('')
        self._updateGrid()

    def _reload(self):
        self.db = Db(self.paths.getLoadPath())

        self.filter_controller.db = self.db
        self.preset_controller.db = self.db
        self.grid_controller.db = self.db

        self.filter_controller.updateLodges()
        self._updateGrid()

    def _updateGrid(self):
        self.grid_controller.updateGrid()

def homePage(paths=Paths(get_save_path())):
    HomePage(paths)
