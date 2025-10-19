from nicegui import binding, ui

from lib.db.db import Db
from lib.ui.components.filter_ui import FilterUi


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
            self._presetSelect = ui.select(options=self.db.presets(), label='preset',
                                           on_change=lambda e : self._applyPreset(e.value)).classes('w-48')
            ui.button(text='+', on_click=self.addPresetDialog.open)
            ui.button(text='-', on_click=self._removePreset)

    def _removePreset(self):
        self.db.presetRemove(self._presetSelect.value)
        self._updatePresets()

    def _addPreset(self):
        self.filter_ui.update_queries_from_filters()
        self.db.presetAdd(self.presetName.text, self.filter_ui.queries.queryDict)
        self._updatePresets()
        self.addPresetDialog.close()

    def _updatePresets(self):
        new_presets = self.db.presets()
        self._presetSelect.set_options(new_presets)
        self._presetSelect.set_value(list(new_presets.keys())[-1])

    def _applyPreset(self, presetValue):
        self.filter_ui.clear_form()
        preset = self.db.preset(presetValue)
        self.filter_ui.update_filters_from_preset(preset)

    def applyCurrentPreset(self):
        self._applyPreset(self._presetSelect.value)

    def clearPresetSelect(self):
        self._presetSelect.set_value('')
