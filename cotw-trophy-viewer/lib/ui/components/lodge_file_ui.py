import tempfile
from pathlib import Path
from typing import Callable

from nicegui import ui

from lib.load.loader import Loader
from lib.ui.utils.auto_reload import AutoReload


class LodgeFileUi:
    def __init__(self, loader: Loader, reloadCallback: Callable):
        self._loader = loader
        self._reloadCallback = reloadCallback
        self._autoReload = AutoReload(loader, self._reloadCallback)
        self._build_ui()

    def _build_ui(self):
        with ui.card():
            with ui.row():
                with ui.card():
                    self.status_label = ui.label()
                    self.status_label.bind_text_from(self, 'status')
                if self._loader.loadFileExists():
                    ui.checkbox(text='auto reload', on_change=self._autoReload.updateAutoReload).set_value(True)

            self.upload_component = (ui
                                     .upload(label='UPLOAD LODGE FILE',
                                             on_upload=self._loadLodgeFile,
                                             multiple=False,
                                             auto_upload=True)
                                     .props('accept="*"')
                                     .tooltip('Upload trophy_lodges_adf file'))
            with ui.row():
                ui.button(text='RESET', on_click=self._reset)
                ui.button(text='RELOAD', on_click=self._reloadCallback)

    @property
    def status(self) -> str:
        return 'LODGE FILE ' + ('FOUND' if self._loader.loadFileExists() else 'NOT FOUND')

    def _loadLodgeFile(self, e):
        if e.content:
            temp_dir = Path(tempfile.mkdtemp())
            temp_file_path = temp_dir / 'trophy_lodges_adf'

            with open(temp_file_path, 'wb') as f:
                e.content.seek(0)
                f.write(e.content.read())

            self._loader.updateLoadPath(temp_file_path)
            self._reloadCallback()

    def _reset(self):
        self._loader.resetToDefaultPath()
        self.upload_component.reset()
        self._reloadCallback()
