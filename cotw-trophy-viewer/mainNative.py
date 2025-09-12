from nicegui import ui

from lib.ui.homePage import homePage

@ui.page("/")
def home():
    homePage()

ui.run(native=True, reload=False, window_size=(1200, 800), title="cotw: Trophy Viewer")