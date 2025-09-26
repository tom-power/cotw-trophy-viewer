from nicegui import ui

from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.ui.controller.filter_controller import FilterController
from lib.ui.controller.grid_controller import GridController
from lib.ui.controller.lodge_file_controller import LodgeFileController
from lib.ui.controller.preset_controller import PresetController
from lib.ui.controller.theme_controller import ThemeController
from lib.ui.utils.formFilter import footer
from lib.ui.utils.paths import Paths


class HomePage:

    def __init__(self, paths: Paths):
        self.paths = paths
        self.db = Db(self.paths.getLoadPath())

        self.filter_controller = None
        self.preset_controller = None
        self.lodge_file_controller = None
        self.grid_controller = None

        self._build_ui()

    def _build_ui(self):
        ThemeController.apply_theme()

        with ui.grid(columns='3fr 1fr').classes('w-full gap-0'):
            self.filter_controller = FilterController(self.db, self._updateGrid, self._clear)

            with ui.card():
                self.lodge_file_controller = LodgeFileController(self.paths, self._reload)
                self.preset_controller = PresetController(self.db, self.filter_controller, self._updateGrid)

            self.grid_controller = GridController(self.db, self.filter_controller)

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
