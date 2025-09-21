import tempfile
from pathlib import Path

from nicegui import ui

from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.model.constants import RATING_BADGES, getKeyFor, presets
from lib.ui.utils.formFilter import footer, select, andOrRadio, reservesOptions, badgeOptions, animalsOptions
from lib.ui.utils.paths import Paths
from lib.ui.utils.queries import Queries
from lib.ui.utils.rowData import rowData


def homePage(paths=Paths(get_save_path())):
    trophyFileExists = paths.getLoadPath() and paths.getLoadPath().exists()
    queries = Queries()
    db = Db(paths.getLoadPath())

    def getDb():
        nonlocal db
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
            ui.notify('Trophy file uploaded successfully!', type='positive')

    def reset():
        paths.resetToDefaultPath()
        upload_component.reset()

    with ui.grid(columns='3fr 1fr').classes('w-full gap-0'):
        with ui.card():  # filter
            with ui.grid(columns='auto auto 600px'):
                ui.space()
                ui.space()
                selectLodges = select(db.lodges(), "lodge", queries.updateQueryFor('lodges'))

                andOrRadio(queries.updateQueryFor('reservesAndOr'))
                ui.space()
                selectReserves = select(reservesOptions(), "reserve", queries.updateQueryFor('reserves'))

                andOrRadio(queries.updateQueryFor('ratingsAndOr'))
                ui.space()
                selectBadges = select(badgeOptions(), "badge", queries.updateQueryFor('ratings'))

                andOrRadio(queries.updateQueryFor('animalsAndOr'))
                ui.space()
                selectAnimals = select(animalsOptions(), "animal", queries.updateQueryFor('animals'))
            with ui.grid(columns='auto 200px 200px'):
                with ui.row():
                    ui.button(text='FILTER', on_click=lambda: updateGrid())
                    ui.button(text='CLEAR', on_click=lambda: clear())
                    checkboxAllAnimals = ui.checkbox(text='All animals')
                ui.space()
                selectPresets = ui.select(options=presets(), label='presets', on_change=lambda e: applyPreset(e))

        with ui.card():  # files
            with ui.card():
                ui.label('LODGE FILE ' + ('FOUND' if trophyFileExists else 'NOT FOUND'))
            upload_component = ui.upload(label='UPLOAD LODGE FILE',
                                         on_upload=lambda e: uploadLodge(e),
                                         multiple=False,
                                         auto_upload=True).props('accept="*"').tooltip('Upload trophy_lodges_adf file')
            with ui.row():
                ui.button(text='RELOAD', on_click=lambda: reload())
                ui.button(text='RESET', on_click=lambda: reset())

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

    def applyPreset(e):
        match e.value:
            case 'diamond checklist':
                clearForm()
                checkboxAllAnimals.set_value(True)
                selectBadges.set_value([(getKeyFor(RATING_BADGES, 'DIAMOND'))])

    def clearForm():
        selectLodges.set_value('')
        selectReserves.set_value('')
        selectBadges.set_value('')
        selectAnimals.set_value('')
        checkboxAllAnimals.set_value(False)

    def clear():
        clearForm()
        selectPresets.set_value('')

    def updateGrid():
        dataGrid.options['rowData'] = getRowData()
        dataGrid.update()

    def reload():
        nonlocal db
        db = Db(paths.getLoadPath())
        selectLodges.set_options(db.lodges())
        updateGrid()

    footer()
