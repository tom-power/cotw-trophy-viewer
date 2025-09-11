import math
from datetime import datetime

from nicegui import ui

from lib.db.db import Db
from lib.model.constants import GENDERS, RESERVES
from lib.ui.utils import getDifficultyName
from lib.ui.utilsUi import footer, dropdown, reservesOptions, animalsOptions, badgeOptions, andOr, checkbox


def homePage():
    db = Db()

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

    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            topControlsGrid = ui.grid(columns=2)

    topButtonRow = ui.row()

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
        'rowData': rowData(db.trophyAnimals(queryDict))
    }, html_columns=[0]).style("height: 600px")

    def updateGrid():
        grid.options['rowData'] = rowData(db.trophyAnimals(queryDict))
        grid.update()

    with topControlsGrid:
        dropdown(db.lodges(), "lodge", updateQueryFor('lodges'))

        andOr(updateQueryFor('reservesAndOr'))
        dropdown(reservesOptions(), "reserve", updateQueryFor('reserves'))

        andOr(updateQueryFor('badgesAndOr'))
        dropdown(badgeOptions(), "badge", updateQueryFor('badge'))

        andOr(updateQueryFor('animalsAndOr'))
        dropdown({0: "ALL"} | animalsOptions(), "animal", updateQueryFor('animals'))
        checkbox('all animals', updateQueryFor('animalsAll'))

    with topButtonRow:
        ui.button('Filter', on_click=lambda: updateGrid())
        ui.button('Refresh', on_click=lambda: homePage())

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