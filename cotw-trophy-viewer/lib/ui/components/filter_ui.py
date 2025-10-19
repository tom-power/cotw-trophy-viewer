from typing import Callable

from nicegui import ui, binding

from lib.db.db import Db
from lib.model.animal_type import AnimalType
from lib.model.animal_type_name import animalName
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.ui.utils.queries import Queries


class FilterUi:
    def __init__(self, db: Db, update_grid_callback: Callable):
        self.db = db
        self.queries = Queries()
        self._update_grid_callback = update_grid_callback
        self._build_ui()

    def _build_ui(self):
        with ui.grid(columns='auto auto 600px'):
            self.checkboxAllAnimals = ui.checkbox(text='Include all animals')
            ui.space()
            self.selectLodges = _selectMulti(self.db.lodges(), 'lodge', )

            self.radioReservesAndOr = _andOrRadio()
            ui.space()
            self.selectReserves = _selectMulti(_reservesOptions(), 'reserve', )

            self.radioMedalsAndOr = _andOrRadio()
            ui.space()
            self.selectMedals = _selectMulti(_medalOptions(), 'medal')

            self.radioAnimalsAndOr = _andOrRadio()
            ui.space()
            self.selectAnimals = _selectMulti(_animalsOptions(), 'animal')

        with ui.row().classes('w-full justify-between items-center'):
            with ui.row():
                ui.button(text='APPLY', on_click=self._update_grid_callback)
                ui.button(text='CLEAR', on_click=self.clear_form)

            self.preset_ui = PresetUi(self)

    def updateLodges(self):
        self.selectLodges.set_options(self.db.lodges(), value=None)

    def update_queries_from_filters(self):
        self.queries.updateQuery('lodges', self.selectLodges.value)
        self.queries.updateQuery('reservesAndOr', self.radioReservesAndOr.value)
        self.queries.updateQuery('reserves', self.selectReserves.value)
        self.queries.updateQuery('medalsAndOr', self.radioMedalsAndOr.value)
        self.queries.updateQuery('medals', self.selectMedals.value)
        self.queries.updateQuery('animalsAndOr', self.radioAnimalsAndOr.value)
        self.queries.updateQuery('animals', self.selectAnimals.value)
        self.queries.updateQuery('allAnimals', self.checkboxAllAnimals.value)

    def update_filters_from_preset(self, preset: dict):
        self.selectLodges.set_value(preset['lodges'])
        self.radioReservesAndOr.set_value(preset['reservesAndOr'])
        self.selectReserves.set_value(preset['reserves'])
        self.radioMedalsAndOr.set_value(preset['medalsAndOr'])
        self.selectMedals.set_value(preset['medals'])
        self.radioAnimalsAndOr.set_value(preset['animalsAndOr'])
        self.selectAnimals.set_value(preset['animals'])
        self.checkboxAllAnimals.set_value(preset['allAnimals'])

    def clear_form(self):
        self.selectLodges.set_value('')
        self.radioReservesAndOr.set_value('and')
        self.selectReserves.set_value('')
        self.radioMedalsAndOr.set_value('and')
        self.selectMedals.set_value('')
        self.radioAnimalsAndOr.set_value('and')
        self.selectAnimals.set_value('')
        self.checkboxAllAnimals.set_value('')
        self.checkboxAllAnimals.set_value(False)

    def applyCurrentPreset(self):
        self.preset_ui.applyCurrentPreset()


def _reservesOptions() -> dict:
    return {r.value: r.reserveName() for r in Reserve}


def _medalOptions() -> dict:
    return {m.value: m.name for m in Medal}


def _animalsOptions() -> dict:
    return {a.value: animalName(a) for a in AnimalType}


def _andOrRadio():
    return ui.radio(['and', 'or'], value='and').props('inline')


def _selectMulti(options, label):
    return ui.select(options=options, multiple=True, label=label, with_input=True, clearable=True).props('use-chips')


class PresetUi:
    @binding.bindable_dataclass
    class PresetName:
        text: str

    def __init__(self, filter_ui: FilterUi):
        self.db: Db = filter_ui.db
        self.filter_ui: FilterUi = filter_ui
        self.presetName = self.PresetName(text="")
        self._build_ui()

    def _build_ui(self):
        self.addPresetDialog = ui.dialog()
        with self.addPresetDialog, ui.card():
            ui.input(label="preset name").bind_value(self.presetName, "text")
            ui.button(text="save", on_click=self._addPreset)

        with ui.row():
            self.selectPresets = ui.select(options=self.db.presets(), label='preset',
                                           on_change=lambda e : self._applyPreset(e.value)).classes('w-48')
            ui.button(text='+', on_click=self.addPresetDialog.open)
            ui.button(text='-', on_click=self._removePreset)

    def _removePreset(self):
        self.db.presetRemove(self.selectPresets.value)
        self._updatePresets()

    def _addPreset(self):
        self.filter_ui.update_queries_from_filters()
        self.db.presetAdd(self.presetName.text, self.filter_ui.queries.queryDict)
        self._updatePresets()
        self.addPresetDialog.close()

    def _updatePresets(self):
        new_presets = self.db.presets()
        self.selectPresets.set_options(new_presets)
        self.selectPresets.set_value(list(new_presets.keys())[-1])

    def _applyPreset(self, presetValue):
        self.filter_ui.clear_form()
        preset = self.db.preset(presetValue)
        self.filter_ui.update_filters_from_preset(preset)

    def applyCurrentPreset(self):
        self._applyPreset(self.selectPresets.value)
