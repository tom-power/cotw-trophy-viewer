import tempfile
from pathlib import Path

from nicegui import ui

from lib.load.loader import Loader


class LodgeFileUi:
    def __init__(self, loader: Loader, reloadFromFile):
        self.loader = loader
        self.reloadFromFile = reloadFromFile
        self._build_ui()

    def _build_ui(self):
        with (ui.card()):
            with ui.card():
                self.status_label = ui.label()
                self.status_label.bind_text_from(self, 'status')
            self.upload_component = ui.upload(label='UPLOAD LODGE FILE',
                                              on_upload=self._loadLodgeFile,
                                              multiple=False,
                                              auto_upload=True
                                              ).props('accept="*"').tooltip('Upload trophy_lodges_adf file')
            with ui.row():
                ui.button(text='RESET', on_click=self._reset)
                ui.button(text='RELOAD', on_click=self._reload)

    @property
    def status(self) -> str:
        return 'LODGE FILE ' + ('FOUND' if self.loader.loadFileExists() else 'NOT FOUND')

    def _loadLodgeFile(self, e):
        if e.content:
            temp_dir = Path(tempfile.mkdtemp())
            temp_file_path = temp_dir / 'trophy_lodges_adf'

            with open(temp_file_path, 'wb') as f:
                e.content.seek(0)  # Reset file pointer to beginning
                f.write(e.content.read())

            self.loader.updateLoadPath(temp_file_path)
            self._reload()
            ui.notify('Trophy file uploaded successfully!', type='positive')

    def _reset(self):
        self.loader.resetToDefaultPath()
        self.upload_component.reset()
        self._reload()
        ui.notify('Reset successfully!', type='positive')

    def _reload(self):
        self.reloadFromFile()
