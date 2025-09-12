import tempfile
from pathlib import Path

from nicegui import ui

from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.ui.utils.data import rowData
from lib.ui.utils.formFilter import footer, dropdown, reservesOptions, animalsOptions, badgeOptions, andOr, uiFormFilter
from lib.ui.utils.grid import uiTrophyGrid
from lib.ui.utils.paths import Paths
from lib.ui.utils.queries import Queries


def homePage():
    paths = Paths(get_save_path())
    queries = Queries()

    def getDb():
        return Db(paths.getLoadPath())

    def getRowData() -> list[dict]:
        return rowData(getDb().trophyAnimals(queries.queryDict))

    async def uploadLodge(e):
        if e.content:
            temp_dir = Path(tempfile.mkdtemp())
            temp_file_path = temp_dir / "trophy_lodges_adf"

            with open(temp_file_path, 'wb') as f:
                e.content.seek(0)  # Reset file pointer to beginning
                f.write(e.content.read())

            paths.updateLoadPath(temp_dir)
            ui.notify('Trophy file uploaded successfully! Using uploaded data.', type='positive')
        updateGrid()

    def resetLodge():
        paths.resetToDefaultPath()
        updateGrid()

    with ui.card():
        with ui.grid(columns='150px auto'):
            uiFormFilter(getDb(), queries)
        with ui.row():
            ui.button(text='FILTER', on_click=lambda: updateGrid())
    with ui.card():
        with ui.row():
            ui.upload(label='UPLOAD LODGE',
                      on_upload=lambda e: uploadLodge(e),
                      multiple=False,
                      auto_upload=True).props('accept="*"').tooltip('Upload trophy_lodges_adf file')
            ui.button(text='RESET LODGE', on_click=lambda: resetLodge())

    grid = uiTrophyGrid(lambda: getRowData())

    def updateGrid():
        grid.options['rowData'] = getRowData()
        grid.update()

    footer()
