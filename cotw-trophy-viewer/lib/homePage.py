from nicegui import ui

from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.load.loader import Loader
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
        self.db = Db()
        self.loader = Loader(self.paths.getLoadPath())
        self.db.load(self.loader)
        self._build_ui()

    def _build_ui(self):
        ThemeUi.apply_theme()

        with ui.grid(columns='800px 1fr 390px').classes('w-full gap-0'):
            self.filter_ui = FilterUi(self.db, self._updateGrid, self._clear)

            ui.space()

            with ui.card():
                LodgeFileUi(self.paths, self._reloadFromFile)
                self.preset_ui = PresetUi(self.db, self.filter_ui, self._updateGrid)

        self.grid_ui = DataGridUi(self.db, self.filter_ui)

    def _clear(self):
        self.filter_ui.clear_form()
        self.preset_ui.selectPresets.set_value('')
        self._updateGrid()

    def _reloadFromFile(self):
        self.db.load(self.loader)

        self.filter_ui.db = self.db
        self.filter_ui.updateLodges()

        self.grid_ui.db = self.db
        self._updateGrid()

    def _updateGrid(self):
        self.grid_ui.updateGrid()


def homePage(paths=Paths(get_save_path())):
    HomePage(paths)
