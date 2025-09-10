import math
from datetime import datetime

from nicegui import ui

from lib.db.db import Db
from lib.model.constants import GENDERS, RATING_BADGES, RESERVES
from lib.ui.utils import getDifficultyName
from lib.ui.utilsUi import footer, dropdownFor, reservesOptions, animalsOptions, badgeOptions



def homePage():

    db=Db()

    lodgesSelected = []
    reservesSelected = []
    animalsSelected = []
    def update(listToUpdate, value):
        listToUpdate.clear()
        listToUpdate += value


    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            ui.label("TROPHIES").style("font-size:30px;color:#666;")
    with ui.row():
        dropdownFor(db.lodges(), "lodge", lambda e: update(lodgesSelected, e.value))
        dropdownFor(reservesOptions(), "reserve", lambda e: update(reservesSelected, e.value))
        dropdownFor({0:"ALL"} | animalsOptions(), "animal", lambda e: update(animalsSelected, e.value))
        dropdownFor(badgeOptions(), "badge", lambda e: e)

    def rowData():
        rows = []
        sortedTrophyAnimals = sorted(db.trophyAnimals(lodgesSelected, reservesSelected, animalsSelected), key=lambda d: d.datetime, reverse=True)

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
                "badge": RATING_BADGES[animal.rating] if RATING_BADGES.__contains__(animal.rating) else 'UNKNOWN',
                "rating": math.floor(animal.rating * 100) / 100,
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

    ui.button('Update', on_click=lambda : updateGrid())

    footer()
