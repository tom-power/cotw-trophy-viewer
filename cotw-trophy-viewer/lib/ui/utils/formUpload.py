from nicegui import ui


def formUploads():
    ui.upload(label='UPLOAD LODGE',
              on_upload=lambda e: uploadLodge(e),
              multiple=False,
              auto_upload=True).props('accept="*"').tooltip('Upload trophy_lodges_adf file')
    ui.button(text='RESET LODGE', on_click=lambda: resetLodge())