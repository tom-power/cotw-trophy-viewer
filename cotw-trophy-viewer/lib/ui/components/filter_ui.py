from datetime import datetime
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
            self.checkboxAllAnimals = ui.checkbox(text='Include all animals', on_change=self._updateFromFilter)
            ui.space()
            self.selectLodges = self._selectMulti(self.db.lodges(), 'lodge', )

            self.radioReservesAndOr = self._andOrRadio()
            ui.space()
            self.selectReserves = self._selectMulti(_reservesOptions(), 'reserve', )

            self.radioMedalsAndOr = self._andOrRadio()
            ui.space()
            self.selectMedals = self._selectMulti(_medalOptions(), 'medal')

            self.radioAnimalsAndOr = self._andOrRadio()
            ui.space()
            self.selectAnimals = self._selectMulti(_animalsOptions(), 'animal')

        with ui.row().classes('w-full justify-between items-center'):
            with ui.row():
                ui.button(text='CLEAR', on_click=self.clear_form_and_preset)

            self.preset_ui = PresetUi(self)

    def _andOrRadio(self):
        return ui.radio(['and', 'or'], value='and', on_change=self._updateFromFilter).props('inline')

    def _selectMulti(self, options, label):
        return ui.select(options=options, multiple=True, label=label, with_input=True, clearable=True,
                         on_change=self._updateFromFilter).props('use-chips')

    def _updateFromFilter(self):
        self._update_grid_callback()
        # self.preset_ui.updatePreset()

    def updateAndSelectLodges(self):
        lodges = self.selectLodges.value
        self.selectLodges.set_options(self.db.lodges(), value=None)
        self.selectLodges.set_value(lodges)

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

    def clear_form_and_preset(self):
        self.clear_form()
        self.preset_ui.clearPresetSelect()

    def clear_form(self):
        self.selectLodges.set_value([])
        self.radioReservesAndOr.set_value('and')
        self.selectReserves.set_value([])
        self.radioMedalsAndOr.set_value('and')
        self.selectMedals.set_value([])
        self.radioAnimalsAndOr.set_value('and')
        self.selectAnimals.set_value([])
        self.checkboxAllAnimals.set_value(False)


def _reservesOptions() -> dict:
    return {r.value: r.reserveName() for r in Reserve}


def _medalOptions() -> dict:
    return {m.value: m.name for m in Medal}


def _animalsOptions() -> dict:
    return {a.value: animalName(a) for a in AnimalType}

class PresetUi:
    class PresetDialogName:
        def __init__(self):
            self.text = ""

    def __init__(self, filter_ui: FilterUi):
        self.db: Db = filter_ui.db
        self.filter_ui: FilterUi = filter_ui
        self.presetDialogName = self.PresetDialogName()
        self._build_ui()

    def _build_ui(self):
        with ui.row():
            self._presetSelect = ui.select(options=self.db.presets(), label='preset',
                                           on_change=lambda e: self._applyPreset(e.value)).classes('w-48')
            ui.button(text='⎙', on_click=self._savePresetWithDialog).classes('size-9')
            ui.button(text='+', on_click=self._addPreset).classes('size-9')
            ui.button(text='-', on_click=self._removePreset).classes('size-9')

    def _savePresetWithDialog(self):
        self._addSavePresetDialog()
        self.savePresetDialog.open()

    def _addSavePresetDialog(self):
        with ui.dialog() as self.savePresetDialog, ui.card():
            text = ""
            if self._presetSelect.value:
                text = self._presetSelect.options[self._presetSelect.value]
            ui.input(label="preset name").bind_value(self.presetDialogName, "text").set_value(text)
            ui.button(text="save", on_click=self._savePresetAndCloseDialog)

    def _savePresetAndCloseDialog(self):
        self._savePresetWithCurrent()
        self.savePresetDialog.close()

    def _savePresetWithCurrent(self):
        self.filter_ui.update_queries_from_filters()
        self.db.presetUpdate(self._presetSelect.value, self.presetDialogName.text, self.filter_ui.queries.queryDict)
        self._updatePresets()
        self._presetSelect.set_value(self._presetSelect.value)

    def _addPreset(self):
        self.filter_ui.update_queries_from_filters()
        self.db.presetAdd('new preset', self.filter_ui.queries.queryDict)
        self._updatePresets()
        self._presetSelect.set_value(list(self.db.presets())[-1])

    def _removePreset(self):
        self.db.presetRemove(self._presetSelect.value)
        self._updatePresets()
        self._presetSelect.set_value(list(self.db.presets())[-1])

    def _updatePresets(self):
        new_presets = self.db.presets()
        self._presetSelect.set_options(new_presets)

    def _applyPreset(self, presetValue):
        if presetValue is not None and str(presetValue) != '':
            self.filter_ui.clear_form()
            preset = self.db.preset(presetValue)
            self.filter_ui.update_filters_from_preset(preset)

    def clearPresetSelect(self):
        self._presetSelect.set_value('')
