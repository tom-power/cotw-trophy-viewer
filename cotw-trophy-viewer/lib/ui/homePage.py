import tempfile
from pathlib import Path

from nicegui import ui

from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.ui.utils.data import rowData
from lib.ui.utils.formFilter import footer, uiFormFilter
from lib.ui.utils.grid import uiTrophyGrid
from lib.ui.utils.paths import Paths
from lib.ui.utils.queries import Queries


def homePage():
    paths = Paths(get_save_path())
    trophyFileExists = paths.getLoadPath() and paths.getLoadPath().exists()
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

    with ui.grid(columns='800px auto'):
        with ui.card(): # filter
            with ui.grid(columns='150px 600px'):
                uiFormFilter(getDb(), queries)
            with ui.row():
                ui.button(text='FILTER', on_click=lambda: updateGrid())
        with ui.card(): # files
            with ui.row():
                with ui.card():
                    ui.label('COTW SAVE FILE -> ' + ('FOUND' if trophyFileExists else 'NOT FOUND'))
            with ui.card():
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
