import tempfile
from pathlib import Path

from nicegui import ui

from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.ui.utils.data import rowData
from lib.ui.utils.formFilter import footer, uiFormFilter
from lib.ui.utils.paths import Paths
from lib.ui.utils.queries import Queries


def homePage(paths=Paths(get_save_path())):
    trophyFileExists = paths.getLoadPath() and paths.getLoadPath().exists()
    queries = Queries()
    db = Db(paths.getLoadPath())

    def reloadDb():
        db = Db(paths.getLoadPath())

    def getDb():
        return db

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

    def resetLodge():
        paths.resetToDefaultPath()

    with ui.grid(columns='3fr 1fr').classes('w-full gap-0'):
        with ui.card():  # filter
            with ui.grid(columns='auto 600px'):
                uiFormFilter(getDb(), queries)
            with ui.row():
                ui.button(text='FILTER', on_click=lambda: updateGrid())
        with ui.card():  # files
            with ui.card():
                ui.label('LODGE FILE ' + ('FOUND' if trophyFileExists else 'NOT FOUND'))
            ui.upload(label='UPLOAD LODGE FILE',
                      on_upload=lambda e: uploadLodge(e),
                      multiple=False,
                      auto_upload=True).props('accept="*"').tooltip('Upload trophy_lodges_adf file')
            ui.button(text='RESET', on_click=lambda: resetLodge())
            ui.button(text='RELOAD', on_click=lambda: reloadDb())

        dataGrid = ui.aggrid({
            'defaultColDef': {'sortable': True},
            'columnDefs': [
                {'headerName': 'Lodge', 'field': 'lodge'},
                {'headerName': 'Reserve', 'field': 'reserve'},
                {'headerName': 'Animal', 'field': 'animal'},
                {'headerName': 'Badge', 'field': 'badge', 'width': '100'},
                {'headerName': 'Score', 'field': 'score', 'width': '100'},
                {'headerName': 'Weight', 'field': 'weight', 'width': '100'},
                {'headerName': 'Datetime', 'field': 'datetime', 'sort': 'desc'},
            ],
            'pagination': True,
            'paginationPageSize': 50,
            'rowData': (lambda: getRowData())()
        }, html_columns=[0]).style("height: 600px").classes('col-span-full border p-1')

    def updateGrid():
        dataGrid.options['rowData'] = getRowData()
        dataGrid.update()

    footer()
