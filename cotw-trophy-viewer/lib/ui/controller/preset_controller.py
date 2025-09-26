from nicegui import ui, binding

from lib.db.db import Db
from lib.ui.controller.filter_controller import FilterController


class PresetController:
    @binding.bindable_dataclass
    class PresetName:
        text: str

    def __init__(self, db: Db, filter_controller: FilterController, update_grid_callback):
        self.db = db
        self.filter_controller = filter_controller
        self.update_grid_callback = update_grid_callback
        self.presetName = self.PresetName(text="")
        self._build_ui()

    def _build_ui(self):
        self.addPresetDialog = ui.dialog()
        with self.addPresetDialog, ui.card():
            ui.input(label="preset name").bind_value(self.presetName, "text")
            ui.button(text="save", on_click=self._addPreset)

        with ui.card():
            with ui.row():
                self.selectPresets = ui.select(options=self.db.presets(), label='presets',
                                               on_change=self._applyPreset).classes('w-48')
                ui.button(text='+', on_click=self.addPresetDialog.open)
                ui.button(text='-', on_click=self._removePreset)

    def _removePreset(self):
        self.db.presetRemove(self.selectPresets.value)
        self._updatePresets()

    def _addPreset(self):
        self.filter_controller.update_queries_from_filters()
        self.db.presetAdd(self.presetName.text, self.filter_controller.queries.queryDict)
        self._updatePresets()
        self.addPresetDialog.close()

    def _updatePresets(self):
        new_presets = self.db.presets()
        self.selectPresets.set_options(new_presets)
        self.selectPresets.set_value(list(new_presets.keys())[-1])

    def _applyPreset(self, e):
        self.filter_controller.clear_form()
        preset = self.db.preset(e.value)
        self.filter_controller.update_filters_from_preset(preset)
        self.update_grid_callback()
