from nicegui import ui

from lib.ui.home import homePage

if __name__ == '__main__':
    @ui.page("/")
    def home():
        homePage()

    ui.run(native=True, reload=False, window_size=(1200, 800), title="cotw: Trophy Viewer")
