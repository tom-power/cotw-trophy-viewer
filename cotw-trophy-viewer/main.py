from nicegui import ui

from lib.ui.homePage import homePage


@ui.page("/")
def home():
    homePage()


ui.run(title="cotw: Trophy Viewer", storage_secret='secret')

