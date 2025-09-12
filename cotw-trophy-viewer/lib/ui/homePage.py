import math
from datetime import datetime
from pathlib import Path
import tempfile

from nicegui import ui

from lib.db.db import Db
from lib.deca.config import get_save_path, set_custom_save_path, reset_to_default_save_path
from lib.model.constants import GENDERS, RESERVES
from lib.ui.utils import getDifficultyName
from lib.ui.utilsUi import footer, dropdown, reservesOptions, animalsOptions, badgeOptions, andOr, checkbox


def homePage():
    loadPath = get_save_path()

    def getLoadPath():
        return loadPath

    def getDb():
        return Db(getLoadPath())

    def updateLoadPath(new_path):
        nonlocal loadPath
        loadPath = new_path
        set_custom_save_path(new_path)

    def resetToDefaultPath():
        nonlocal loadPath
        reset_to_default_save_path()
        loadPath = get_save_path()
        ui.notify('Reset to default save path', type='info')
        updateGrid()

    queryDict = {
        'lodges': [],
        'reservesAndOr': 'or',
        'reserves': [],
        'badgesAndOr': 'or',
        'badges': [],
        'animalsAndOr': 'or',
        'animals': [],
        'animalsAll': False,
    }

    def updateQuery(key, value):
        queryDict[key] = value

    def updateQueryFor(key):
        return lambda e: updateQuery(key, e.value)

    with ui.card():
        topControlsGrid = ui.grid(columns='150px auto')
        filterButtonRow = ui.row()
    with ui.card():
        updateResetButtonRow = ui.row()

    grid = ui.aggrid({
        'defaultColDef': {'sortable': True},
        'columnDefs': [
            {'headerName': 'Lodge', 'field': 'lodge', 'width': '80'},
            {'headerName': 'Reserve', 'field': 'reserve', 'width': '250'},
            {'headerName': 'Animal', 'field': 'animal', 'width': '140'},
            {'headerName': 'Badge', 'field': 'badge', 'width': '140'},
            {'headerName': 'Score', 'field': 'score', 'width': '120'},
            {'headerName': 'Weight', 'field': 'weight', 'width': '140'},
            {'headerName': 'Datetime', 'field': 'datetime', 'width': '200', 'sort': 'desc'},
        ],
        'pagination': True,
        'paginationPageSize': 50,
        'rowData': rowData(getDb().trophyAnimals(queryDict))
    }, html_columns=[0]).style("height: 600px")

    def updateGrid():
        grid.options['rowData'] = rowData(getDb().trophyAnimals(queryDict))
        grid.update()

    async def handle_file_upload(e):
        if e.content:
            temp_dir = Path(tempfile.mkdtemp())
            temp_file_path = temp_dir / "trophy_lodges_adf"

            with open(temp_file_path, 'wb') as f:
                e.content.seek(0)  # Reset file pointer to beginning
                f.write(e.content.read())

            updateLoadPath(temp_dir)

            ui.notify('Trophy file uploaded successfully! Using uploaded data.', type='positive')

        updateGrid()

    with topControlsGrid:
        ui.space()
        dropdown(getDb().lodges(), "lodge", updateQueryFor('lodges'))

        andOr(updateQueryFor('reservesAndOr'))
        dropdown(reservesOptions(), "reserve", updateQueryFor('reserves'))

        andOr(updateQueryFor('badgesAndOr'))
        dropdown(badgeOptions(), "badge", updateQueryFor('badge'))

        andOr(updateQueryFor('animalsAndOr'))
        dropdown({0: "ALL"} | animalsOptions(), "animal", updateQueryFor('animals'))

    with filterButtonRow:
        ui.button(text='FILTER', on_click=lambda: updateGrid())

    with updateResetButtonRow:
        ui.upload(label='UPLOAD LODGE',
                  on_upload=handle_file_upload,
                  multiple=False,
                  auto_upload=True).props('accept="*"').tooltip('Upload trophy_lodges_adf file')
        ui.button(text='RESET LODGE', on_click=resetToDefaultPath)

    footer()


def rowData(trophyAnimals) -> [dict]:
    rows = []

    for animal in trophyAnimals:
        furTypeName = "UNKNOWN"

        if hasattr(animal, "furType") and animal.furType is not None:
            furTypeName = animal.furType

        rows.append({
            # "id": idDisplay,
            "lodge": animal.lodge,
            "reserve": list(RESERVES[animal.reserve].keys())[0] if RESERVES.__contains__(
                animal.reserve) else 'UNKNOWN',
            "animal": animal.type,
            "gender": GENDERS[animal.gender] if GENDERS.__contains__(animal.gender) else 'UNKNOWN',
            "weight": round(animal.weight * 100) / 100,
            "rating": math.floor(animal.rating * 100) / 100,
            "badge": animal.badge,
            "difficulty": getDifficultyName(animal.difficulty),
            "difficultyScore": math.floor(animal.difficulty * 1000) / 1000,
            "furType": furTypeName,
            "score": animal.score,
            "datetime": datetime.fromtimestamp(int(animal.datetime)),
        })
    return rows
