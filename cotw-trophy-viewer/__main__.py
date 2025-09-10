from nicegui import ui

from lib.deca.config import get_save_path
from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from lib.ui.home import homePage

if __name__ == '__main__':



    @ui.page("/")
    def home():
        homePage()

    ui.run(native=True, reload=False, window_size=(1200, 800), title="cotw: Trophy Viewer")
