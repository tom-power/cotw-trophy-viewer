import math
from typing import List

from nicegui import ui

from lib.model.constants import GENDERS, RATING_BADGES
from lib.model.trophyanimal import TrophyAnimal
from lib.ui.utils import getDifficultyName
from lib.ui.utilsUi import footer, headerHome


def homePage(trophyAnimals: List[TrophyAnimal]):
    headerHome()

    rowData = []
    maxLatestAnimals = 50

    sortedTrophyAnimals = sorted(trophyAnimals, key=lambda d: d.datetime, reverse=True)

    for animal in sortedTrophyAnimals:
        furTypeName = "UNKNOWN"

        if hasattr(animal, "furType") and animal.furType is not None:
            furTypeName = animal.furType

        rowData.append({
            # "id": idDisplay,
            "animal": animal.type,
            "gender": GENDERS[animal.gender] if GENDERS.__contains__(animal.gender) else 'UNKNOWN',
            "weight": round(animal.weight * 100) / 100,
            "badge": RATING_BADGES[animal.rating] if RATING_BADGES.__contains__(animal.rating) else 'UNKNOWN',
            "rating": math.floor(animal.rating * 100) / 100,
            "difficulty": getDifficultyName(animal.difficulty),
            "difficultyScore": math.floor(animal.difficulty * 1000) / 1000,
            "furType": furTypeName,
            "score": animal.score,
            "datetime": animal.datetime,
            "lodge": animal.lodge,
            "reserve": animal.reserve,

        })

        maxLatestAnimals = maxLatestAnimals - 1
        if maxLatestAnimals == 0:
            break

    ui.aggrid({
        'defaultColDef': {'sortable': True},
        'columnDefs': [
            {'headerName': 'Animal', 'field': 'animal'},
            {'headerName': 'Gender', 'field': 'gender', 'width': '140'},
            {'headerName': 'Badge', 'field': 'badge', 'width': '140'},
            {'headerName': 'Rating', 'field': 'rating', 'width': '140'},
            {'headerName': 'Difficulty', 'field': 'difficulty'},
            {'headerName': 'Difficulty Score', 'field': 'difficultyScore'},
            {'headerName': 'Fur Type', 'field': 'furType'},
            {'headerName': 'Weight', 'field': 'weight', 'width': '140'},
            {'headerName': 'Score', 'field': 'score', 'width': '120'},
            {'headerName': 'Reserve', 'field': 'reserve', 'width': '120'},
            {'headerName': 'Lodge', 'field': 'lodge', 'width': '120'},
            {'headerName': 'Datetime', 'field': 'datetime', 'width': '300', 'sort': 'desc'},
        ],
        'pagination': True,
        'paginationPageSize': 50,
        'rowData': rowData
    }, html_columns=[0]).style("height: 600px")

    footer()
