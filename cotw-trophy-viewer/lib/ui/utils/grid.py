from typing import Callable, List

from nicegui import ui

from lib.model.animalType import AnimalType
from lib.model.constants import RATING_BADGES
from lib.model.reserve import ReserveEnum


def uiTrophyGrid(rowData: Callable[[], List[dict]]):
    return ui.aggrid({
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