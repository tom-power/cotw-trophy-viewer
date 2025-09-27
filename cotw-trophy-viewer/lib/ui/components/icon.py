import sys
from pathlib import Path

from nicegui import ui

APP_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent.parent.parent))

class Icon:
    def __init__(self):
        ui.image(source=Path(APP_DIR_PATH / 'assets/main-logo.png'))
