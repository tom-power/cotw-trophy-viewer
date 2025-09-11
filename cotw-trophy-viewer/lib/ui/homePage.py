import math
from datetime import datetime

from nicegui import ui

from lib.db.db import Db
from lib.model.constants import GENDERS, RATING_BADGES, RESERVES
from lib.ui.utils import getDifficultyName
from lib.ui.utilsUi import footer, dropdown, reservesOptions, animalsOptions, badgeOptions, andOr, checkbox


def homePage():
    db = Db()

    queryDict = {
        'lodges': [],
        'lodgesAndOr': 'or',
        'reserves': [],
        'reservesAndOr': 'or',
        'animals': [],
        'animalsAndOr': 'or',
        'badges': [],
        'animalsAll': False,
    }

    def updateQuery(key, value):
        queryDict[key] = value

    topGrid= ui.grid(columns=2)
    topRow= ui.row()

    def rowData():
        rows = []
        sortedTrophyAnimals = sorted(db.trophyAnimals(queryDict),
                                     key=lambda d: d.datetime, reverse=True)

        for animal in sortedTrophyAnimals:
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
        'rowData': rowData()
    }, html_columns=[0]).style("height: 600px")

    def updateGrid():
        grid.options['rowData'] = rowData()
        grid.update()

    with topGrid:
        dropdown(db.lodges(), "lodge", lambda e: updateQuery('lodges', e.value))
        andOr(lambda e: updateQuery('lodgesAndOr', e.value))
        
        dropdown(reservesOptions(), "reserve", lambda e: updateQuery('reserves', e.value))
        andOr(lambda e: updateQuery('reservesAndOr', e.value))

        dropdown(badgeOptions(), "badge", lambda e: updateQuery('badge', e.value))
        andOr(lambda e: updateQuery('animalsAndOr', e.value))

        dropdown({0: "ALL"} | animalsOptions(), "animal", lambda e: updateQuery('animals', e.value))
        checkbox('all animals', lambda e: updateQuery('animalsAll', e.value))

    with topRow:
        ui.button('Filter', on_click=lambda: updateGrid())
        ui.button('Refresh', on_click=lambda: homePage())

    footer()
