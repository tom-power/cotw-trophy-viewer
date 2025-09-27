from nicegui import ui


class Theme:
    @staticmethod
    def apply_theme():
        ui.colors(primary='#F39C12', secondary='#34495E', accent='#111B1E', positive='#53B689')
