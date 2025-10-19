from pathlib import Path

from nicegui import ui

from lib.db.config import DB_PATH
from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.load.loader import Loader
from lib.ui.components.data_grid_ui import DataGridUi
from lib.ui.components.filter_ui import FilterUi, PresetUi
from lib.ui.components.icon_ui import IconUi
from lib.ui.components.lodge_file_ui import LodgeFileUi
from lib.ui.components.theme_ui import ThemeUi
from lib.ui.utils.paths import Paths


class HomePage:

    def __init__(self, paths: Paths, db_path: Path):
        self.paths = paths
        self.db = Db(db_path)
        self.loader = Loader(self.paths)
        self.db.load(self.loader)
        self._build_ui()

    def _build_ui(self):
        ThemeUi.apply_theme()

        with ui.grid(columns='800px 1fr 390px').classes('w-full gap-0'):
            with ui.card():
                self.filter_ui = FilterUi(self.db, self._updateGrid)

            ui.space()

            with ui.card():
                LodgeFileUi(self.loader, self._reloadFromLodgeFile)
                with ui.row().classes('w-full'):
                    ui.space()
                    IconUi()

        self.grid_ui = DataGridUi(self.db, self.filter_ui)


    def _updateGrid(self):
        self.grid_ui.updateGrid()

    def _reloadFromLodgeFile(self):
        self.db.load(self.loader)

        self.filter_ui.db = self.db
        self.filter_ui.updateLodges()

        self.filter_ui.applyCurrentPreset()

        self.grid_ui.db = self.db
        self._updateGrid()


def homePage(paths=Paths(get_save_path() / 'trophy_lodges_adf'), db_path=DB_PATH):
    HomePage(paths=paths, db_path=db_path)
