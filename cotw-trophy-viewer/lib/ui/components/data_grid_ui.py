from typing import List

from nicegui import ui

from lib.db.db import Db
from lib.model.animal_type import AnimalType
from lib.model.animal_type_name import animalName
from lib.model.difficulty import Difficulty
from lib.model.gender import Gender
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophy_animal import TrophyAnimal
from lib.ui.components.filter_ui import FilterUi


class DataGridUi:
    def __init__(self, db: Db, filter_ui: FilterUi):
        self.db = db
        self.filter_ui = filter_ui
        self._build_ui()

    def _build_ui(self):
        self.dataGrid = ui.aggrid({
            'defaultColDef': {
                'sortable': True,
                'cellDataType': False
            },
            'columnDefs': [
                {'headerName': 'Lodge',
                 'field': 'lodge',
                 'width': '150',
                 'filter': 'agTextColumnFilter'
                 },
                {'headerName': 'Reserve',
                 'field': 'reserve',
                 'filter': 'agTextColumnFilter'
                 },
                {'headerName': 'Animal',
                 'field': 'animal',
                 'filter': 'agTextColumnFilter'
                 },
                {'headerName': 'Weight',
                 'field': 'weight',
                 'width': '100',
                 'filter': 'agNumberColumnFilter'
                 },
                {'headerName': 'Fur type',
                 'field': 'furType',
                 'width': '100',
                 'filter': 'agNumberColumnFilter'
                 },
                {'headerName': 'Difficulty',
                 'field': 'difficulty',
                 'width': '150',
                 'filter': 'agTextColumnFilter'
                 },
                {'headerName': 'Rating',
                 'field': 'rating',
                 'width': '100',
                 'filter': 'agNumberColumnFilter'
                 },
                {'headerName': 'Medal',
                 'field': 'medal',
                 'width': '100',
                 'filter': 'agTextColumnFilter'
                 },
                {'headerName': 'Harvested Date',
                 'field': 'harvestedDate',
                 'width': '175',
                 'sort': 'desc',
                 'valueFormatter': DATE_TIME_FORMAT,
                 'filter': 'agDateColumnFilter',
                 'filterParams': {
                     ':comparator': DATE_TIME_COMPARATOR
                 }
                 },
            ],
            'pagination': True,
            'paginationPageSize': 50,
            'rowData': self._get_row_data()
        },
            html_columns=[0]).style('height: 600px').classes('col-span-full border p-1 ag-theme-balham-dark')

    def _get_row_data(self) -> list[dict]:
        return rowData(self.db.trophyAnimals(self.filter_ui.queries.queryDict))

    def updateGrid(self):
        self.filter_ui.update_queries_from_filters()
        self.dataGrid.options['rowData'] = self._get_row_data()
        self.dataGrid.update()


def rowData(trophyAnimals: List[TrophyAnimal]) -> List[dict]:
    rows = []

    for animal in trophyAnimals:
        rows.append({
            # 'id': idDisplay,
            'lodge': _naIfNone(animal.lodge, lambda l: l.lodgeName()),
            'reserve': _naIfNone(animal.reserve, lambda r: Reserve(r).reserveName()),
            'animal': _naIfNone(animal.type, lambda t: _getAnimalTypeName(t)),
            'gender': _naIfNone(animal.gender, lambda g: Gender(g).name),
            'weight': _naIfNone(animal.weight, lambda w: round(w * 100) / 100),
            'furType': _naIfNone(animal.furType),
            'difficulty': _naIfNone(animal.difficulty, lambda d: Difficulty.getDifficultyName(d)),
            'rating': _naIfNone(animal.rating, lambda r: round(r * 100) / 100),
            'medal': _naIfNone(animal.medal, lambda m: Medal(m).medalName()),
            'harvestedDate': _naIfNone(animal.datetime),
        })
    return rows


def _getAnimalTypeName(key: int) -> str:
    try:
        return animalName(AnimalType(key))
    except ValueError:
        return f'{key}'


def _naIfNone(value, fn=lambda a: a):
    if value is None:
        return 'NA'
    return fn(value)


DATE_TIME_FORMAT = '''(
        value === undefined || value === 'NA' 
            ? 'NA' 
            : 
            new Date(value * 1000)
                .toLocaleDateString(undefined, {hour: \"2-digit\", minute: \"2-digit\"})
                .replace(\",\", \"\")
        )'''

DATE_TIME_COMPARATOR = '''(filterLocalDateAtMidnight, cellValue) => {                     
                            const cellDate = new Date(cellValue * 1000).setHours(0,0,0,0);
                            return cellDate < filterLocalDateAtMidnight ? -1 : cellDate > filterLocalDateAtMidnight ? 1 : 0;
                        }'''
