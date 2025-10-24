from nicegui import ui

def iconButton(text, on_click):
    return ui.button(text=text, on_click=on_click).classes('size-9 mt-2')