from nicegui import ui


class Theme:
    @staticmethod
    def apply_theme():
        ui.dark_mode().enable()
        ui.colors(primary='#F39C12', secondary='#111B1E', accent='#000000', positive='#53B689')
