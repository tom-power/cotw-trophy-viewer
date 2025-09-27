import tempfile
from pathlib import Path

from nicegui import ui


class LodgeFile:
    def __init__(self, paths, reload_callback):
        self.paths = paths
        self.reload_callback = reload_callback
        self._build_ui()

    def _build_ui(self):
        with ui.card():
            with ui.card():
                self.status_label = ui.label()
                self.status_label.bind_text_from(self, 'status')
            self.upload_component = ui.upload(label='UPLOAD LODGE FILE',
                                             on_upload=self._uploadLodge,
                                             multiple=False,
                                             auto_upload=True).props('accept="*"').tooltip(
                'Upload trophy_lodges_adf file')
            with ui.row():
                ui.button(text='RELOAD', on_click=self._reload)
                ui.button(text='RESET', on_click=self._reset)

    @property
    def status(self) -> str:
        exists = self.paths.getLoadPath() and self.paths.getLoadPath().exists()
        return 'LODGE FILE ' + ('FOUND' if exists else 'NOT FOUND')

    async def _uploadLodge(self, e):
        if e.content:
            temp_dir = Path(tempfile.mkdtemp())
            temp_file_path = temp_dir / 'trophy_lodges_adf'

            with open(temp_file_path, 'wb') as f:
                e.content.seek(0)  # Reset file pointer to beginning
                f.write(e.content.read())

            self.paths.updateLoadPath(temp_dir)
            ui.notify('Trophy file uploaded successfully!', type='positive')
            self.reload_callback()

    def _reset(self):
        self.paths.resetToDefaultPath()
        self.upload_component.reset()
        self.reload_callback()

    def _reload(self):
        self.reload_callback()
