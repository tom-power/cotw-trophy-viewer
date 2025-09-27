from nicegui import ui

from lib.db.db import Db
from lib.ui.components.filter import Filter
from lib.ui.utils.rowData import rowData


class Grid:
    def __init__(self, db: Db, filter_controller: Filter):
        self.db = db
        self.filter_controller = filter_controller
        self._build_ui()

    def _build_ui(self):
        self.dataGrid = ui.aggrid({
            'defaultColDef': {'sortable': True},
            'columnDefs': [
                {'headerName': 'Lodge', 'field': 'lodge', 'width': '200'},
                {'headerName': 'Reserve', 'field': 'reserve'},
                {'headerName': 'Medal', 'field': 'medal', 'width': '100'},
                {'headerName': 'Animal', 'field': 'animal'},
                {'headerName': 'Rating', 'field': 'rating', 'width': '100'},
                {'headerName': 'Weight', 'field': 'weight', 'width': '100'},
                {'headerName': 'Difficulty', 'field': 'difficulty', 'width': '100'},
                # {'headerName': 'Fur type', 'field': 'furType', 'width': '100'},
                {'headerName': 'Harvested Date', 'field': 'datetime', 'sort': 'desc'},
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
