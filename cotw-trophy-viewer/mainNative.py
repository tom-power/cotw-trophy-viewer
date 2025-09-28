from nicegui import ui

from lib.ui.homePage import homePage


@ui.page("/")
def home():
    homePage()


ui.run(native=True, reload=False, window_size=(1440, 900), title="cotw: Trophy Viewer")
