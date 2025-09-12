from nicegui import ui

from lib.ui.homePage import homePage

if __name__ == '__main__' or __name__ == '__mp_main__':
    @ui.page("/")
    def home():
        homePage()


    ui.run(title="cotw: Trophy Viewer")
