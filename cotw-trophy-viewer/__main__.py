from nicegui import ui

from lib.deca.config import get_save_path
from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from lib.ui.home import homePage

if __name__ == '__main__':
    trophyAnimals = loadTrophyAnimals(get_save_path())


    @ui.page("/")
    def home():
        homePage(trophyAnimals)


    ui.run(native=True, reload=False, window_size=(1200, 800), title="theHunterCotW: Trophy Viewer")
