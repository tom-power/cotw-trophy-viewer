import tempfile
from pathlib import Path

from nicegui import ui, binding

from lib.db.db import Db
from lib.deca.config import get_save_path
from lib.ui.utils.formFilter import footer, selectMulti, andOrRadio, reservesOptions, medalOptions, animalsOptions
from lib.ui.utils.paths import Paths
from lib.ui.utils.queries import Queries
from lib.ui.utils.rowData import rowData


class HomePage:
    @binding.bindable_dataclass
    class PresetName:
        text: str

    def __init__(self, paths: Paths):
        self.paths = paths
        self.queries = Queries()
        self.db = Db(self.paths.getLoadPath())
        self.trophyFileExists = self.paths.getLoadPath() and self.paths.getLoadPath().exists()

        self.presetName = self.PresetName(text="")

        self.selectLodges = None
        self.radioReservesAndOr = None
        self.selectReserves = None
        self.radioMedalsAndOr = None
        self.selectMedals = None
        self.radioAnimalsAndOr = None
        self.selectAnimals = None
        self.checkboxAllAnimals = None

        self.upload_component = None
        self.selectPresets = None
        self.addPresetDialog = None
        self.dataGrid = None

        self._build_ui()

    def _build_ui(self):
        self.addPresetDialog = ui.dialog()
        with self.addPresetDialog, ui.card():
            ui.input(label="preset name").bind_value(self.presetName, "text")
            ui.button(text="save", on_click=self._addPreset)

        with ui.grid(columns='3fr 1fr').classes('w-full gap-0'):
            with ui.card():
                with ui.grid(columns='auto auto 600px'):
                    ui.space()
                    ui.space()
                    self.selectLodges = selectMulti(self.db.lodges(), 'lodge', )

                    self.radioReservesAndOr = andOrRadio()
                    ui.space()
                    self.selectReserves = selectMulti(reservesOptions(), 'reserve', )

                    self.radioMedalsAndOr = andOrRadio()
                    ui.space()
                    self.selectMedals = selectMulti(medalOptions(), 'medal')

                    self.radioAnimalsAndOr = andOrRadio()
                    ui.space()
                    self.selectAnimals = selectMulti(animalsOptions(), 'animal')

                with ui.row():
                    ui.button(text='FILTER', on_click=self._updateGrid)
                    ui.button(text='CLEAR', on_click=self._clear)
                    self.checkboxAllAnimals = ui.checkbox(text='All animals')

            with ui.card():
                with ui.card():
                    with ui.card():
                        ui.label('LODGE FILE ' + ('FOUND' if self.trophyFileExists else 'NOT FOUND'))
                    self.upload_component = ui.upload(label='UPLOAD LODGE FILE',
                                                 on_upload=self._uploadLodge,
                                                 multiple=False,
                                                 auto_upload=True).props('accept="*"').tooltip(
                        'Upload trophy_lodges_adf file')
                    with ui.row():
                        ui.button(text='RELOAD', on_click=self._reload)
                        ui.button(text='RESET', on_click=self._reset)

                with ui.card():
                    with ui.row():
                        self.selectPresets = ui.select(options=self._presets(), label='presets',
                                                  on_change=self._applyPreset).classes('w-48')
                        ui.button(text='+', on_click=self.addPresetDialog.open)
                        ui.button(text='-', on_click=self._removePreset)

            self.dataGrid = ui.aggrid({
                'defaultColDef': {'sortable': True},
                'columnDefs': [
                    {'headerName': 'Lodge', 'field': 'lodge', 'width': '100'},
                    {'headerName': 'Reserve', 'field': 'reserve'},
                    {'headerName': 'Medal', 'field': 'medal', 'width': '100'},
                    {'headerName': 'Animal', 'field': 'animal'},
                    {'headerName': 'Rating', 'field': 'rating', 'width': '100'},
                    {'headerName': 'Weight', 'field': 'weight', 'width': '100'},
                    {'headerName': 'Difficulty', 'field': 'difficulty', 'width': '100'},
                    {'headerName': 'Fur type', 'field': 'furType', 'width': '100'},
                    {'headerName': 'Datetime', 'field': 'datetime', 'sort': 'desc'},
                ],
                'pagination': True,
                'paginationPageSize': 50,
                'rowData': self._getRowData()
            }, html_columns=[0]).style('height: 600px').classes('col-span-full border p-1')

            footer()

    def _getDb(self):
        return self.db

    def _getRowData(self) -> list[dict]:
        return rowData(self._getDb().trophyAnimals(self.queries.queryDict))

    async def _uploadLodge(self, e):
        if e.content:
            temp_dir = Path(tempfile.mkdtemp())
            temp_file_path = temp_dir / 'trophy_lodges_adf'

            with open(temp_file_path, 'wb') as f:
                e.content.seek(0)  # Reset file pointer to beginning
                f.write(e.content.read())

            self.paths.updateLoadPath(temp_dir)
            ui.notify('Trophy file uploaded successfully!', type='positive')

    def _reset(self):
        self.paths.resetToDefaultPath()
        self.upload_component.reset()

    def _presets(self) -> dict:
        return self.db.presets()

    def _removePreset(self):
        self.db.presetRemove(self.selectPresets.value)
        self._updatePresets()

    def _addPreset(self):
        self._updateQueries()
        self.db.presetAdd(self.presetName.text, self.queries.queryDict)
        self._updatePresets()
        self.addPresetDialog.close()

    def _updatePresets(self):
        new_presets = self.db.presets()
        self.selectPresets.set_options(new_presets)
        self.selectPresets.set_value(list(new_presets.keys())[-1])

    def _applyPreset(self, e):
        self._clearForm()
        preset = self.db.preset(e.value)
        self._updateFilterFromPreset(preset)

    def _updateFilterFromPreset(self, preset: dict):
        self.selectLodges.set_value(preset['lodges'])
        self.radioReservesAndOr.set_value(preset['medals'])
        self.selectReserves.set_value(preset['reserves'])
        self.radioMedalsAndOr.set_value(preset['medalsAndOr'])
        self.selectMedals.set_value(preset['medals'])
        self.radioAnimalsAndOr.set_value(preset['animalsAndOr'])
        self.selectAnimals.set_value(preset['animals'])
        self.checkboxAllAnimals.set_value(preset['allAnimals'])

    def _clearForm(self):
        self.selectLodges.set_value('')
        self.selectReserves.set_value('')
        self.selectMedals.set_value('')
        self.selectAnimals.set_value('')
        self.checkboxAllAnimals.set_value(False)

    def _clear(self):
        self._clearForm()
        self.selectPresets.set_value('')

    def _updateQueries(self):
        self.queries.updateQuery('lodges', self.selectLodges.value)
        self.queries.updateQuery('reservesAndOr', self.radioReservesAndOr.value)
        self.queries.updateQuery('reserves', self.selectReserves.value)
        self.queries.updateQuery('medalsAndOr', self.radioMedalsAndOr.value)
        self.queries.updateQuery('medals', self.selectMedals.value)
        self.queries.updateQuery('animalsAndOr', self.radioAnimalsAndOr.value)
        self.queries.updateQuery('animals', self.selectAnimals.value)
        self.queries.updateQuery('allAnimals', self.checkboxAllAnimals.value)

    def _updateGrid(self):
        self._updateQueries()
        self.dataGrid.options['rowData'] = self._getRowData()
        self.dataGrid.update()

    def _reload(self):
        self.db = Db(self.paths.getLoadPath())
        self.selectLodges.set_options(self.db.lodges())
        self._updateGrid()


def homePage(paths=Paths(get_save_path())):
    HomePage(paths)
