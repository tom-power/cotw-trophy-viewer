import sys
from pathlib import Path

from nicegui import ui

from lib.homePage import homePage

APP_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

@ui.page("/")
def home():
    homePage()


ui.run(title="cotw: Trophy Viewer", favicon=Path(APP_DIR_PATH / 'assets/favico.webp'))

