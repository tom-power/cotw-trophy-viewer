from typing import List

from nicegui import ui

from lib.db.db import Db
from lib.model.animal_type import AnimalType
from lib.model.difficulty import Difficulty
from lib.model.gender import Gender
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophy_animal import TrophyAnimal
from lib.ui.components.filter_ui import FilterUi


class DataGridUi:
    def __init__(self, db: Db, filter_controller: FilterUi):
        self.db = db
        self.filter_controller = filter_controller
        self.TIME_FORMAT = "value === undefined || value === 'NA' ? 'NA' : new Date(value * 1000).toLocaleDateString(undefined, {hour: \"2-digit\", minute: \"2-digit\"}).replace(\",\", \"\")"
        self._build_ui()

    def _build_ui(self):
        self.dataGrid = ui.aggrid({
            'defaultColDef': {'sortable': True},
            'columnDefs': [
                {'headerName': 'Lodge', 'field': 'lodge', 'width': '200'},
                {'headerName': 'Reserve', 'field': 'reserve'},
                {'headerName': 'Animal', 'field': 'animal'},
                {'headerName': 'Weight', 'field': 'weight', 'width': '100'},
                {'headerName': 'Fur type', 'field': 'furType', 'width': '100'},
                {'headerName': 'Difficulty', 'field': 'difficulty', 'width': '150'},
                {'headerName': 'Trophy Rating', 'field': 'rating', 'width': '150'},
                {'headerName': 'Medal', 'field': 'medal', 'width': '100'},
                {'headerName': 'Harvested Date', 'field': 'datetime', 'sort': 'desc',
                 'valueFormatter': self.TIME_FORMAT},
            ],
            'pagination': True,
            'paginationPageSize': 50,
            'rowData': self._get_row_data()
        }, html_columns=[0]).style('height: 600px').classes('col-span-full border p-1 ag-theme-balham-dark')

    def _get_row_data(self) -> list[dict]:
        return rowData(self.db.trophyAnimals(self.filter_controller.queries.queryDict))

    def updateGrid(self):
        self.filter_controller.update_queries_from_filters()
        self.dataGrid.options['rowData'] = self._get_row_data()
        self.dataGrid.update()


def rowData(trophyAnimals: List[TrophyAnimal]) -> List[dict]:
    rows = []

    for animal in trophyAnimals:
        furTypeName = 'UNKNOWN'

        if hasattr(animal, 'furType') and animal.furType is not None:
            furTypeName = animal.furType

        rows.append({
            # 'id': idDisplay,
            'lodge': _naIfNone(animal.lodge, lambda l: l.lodgeName()),
            'reserve': _naIfNone(animal.reserve, lambda r: Reserve(r).reserveName()),
            'animal': _naIfNone(animal.type, lambda t: _getAnimalTypeName(t)),
            'gender': _naIfNone(animal.gender, lambda g: Gender(g).name),
            'weight': _naIfNone(animal.weight, lambda w: round(w * 100) / 100),
            'furType': _naIfNone(furTypeName),
            'difficulty': _naIfNone(animal.difficulty, lambda d: Difficulty.getDifficultyName(d)),
            'rating': _naIfNone(animal.rating, lambda r: round(r * 100) / 100),
            'medal': _naIfNone(animal.medal, lambda m: Medal(m).medalName()),
            'datetime': _naIfNone(animal.datetime)            ,
        })
    return rows


def _getAnimalTypeName(key: int) -> str:
    try:
        return AnimalType(key).animalName()
    except ValueError:
        return f'{key}'


def _naIfNone(value, fn=lambda a: a):
    if value is None:
        return 'NA'
    return fn(value)
