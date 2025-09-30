from nicegui import ui

from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.load.loader import Loader
from lib.ui.components.data_grid_ui import DataGridUi
from lib.ui.components.filter_ui import FilterUi
from lib.ui.components.lodge_file_ui import LodgeFileUi
from lib.ui.components.preset_ui import PresetUi
from lib.ui.components.theme_ui import ThemeUi
from lib.hub import Hub
from lib.ui.utils.formFilter import footer
from lib.ui.utils.paths import Paths


class HomePage:

    def __init__(self, paths: Paths):
        self.paths = paths
        self.hub = Hub(Db(), Loader(self.paths.getLoadPath()))

        self._build_ui()

    def _build_ui(self):
        ThemeUi.apply_theme()

        with ui.grid(columns='800px 1fr 390px').classes('w-full gap-0'):
            self.filter_ui = FilterUi(self.hub, self._updateGrid, self._clear)

            ui.space()

            with ui.card():
                LodgeFileUi(self.paths, self._reload)
                self.preset_ui = PresetUi(self.hub, self.filter_ui, self._updateGrid)

        self.grid_ui = DataGridUi(self.hub, self.filter_ui)

        footer()

    def _clear(self):
        self.filter_ui.clear_form()
        self.preset_ui.selectPresets.set_value('')
        self._updateGrid()

    def _reload(self):
        self.hub = Hub(Db(), Loader(self.paths.getLoadPath()))

        self.filter_ui.hub = self.hub
        self.preset_ui.hub = self.hub
        self.grid_ui.hub = self.hub

        self.filter_ui.updateLodges()
        self._updateGrid()

    def _updateGrid(self):
        self.grid_ui.updateGrid()

def homePage(paths=Paths(get_save_path())):
    HomePage(paths)
