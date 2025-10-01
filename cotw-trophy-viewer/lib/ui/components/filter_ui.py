
from nicegui import ui

from lib.ui.components.icon_ui import IconUi
from lib.db.db import Db
from lib.ui.utils.formFilter import selectMulti, andOrRadio, reservesOptions, medalOptions, animalsOptions
from lib.ui.utils.queries import Queries


class FilterUi:
    def __init__(self, db: Db, filter_callback, clear_callback):
        self.db = db
        self.queries = Queries()
        self.filter_callback = filter_callback
        self.clear_callback = clear_callback
        self._build_ui()

    def _build_ui(self):
        with ui.card():
            with ui.grid(columns='auto auto 600px'):
                ui.space()
                ui.space()
                self.selectLodges = selectMulti(self.db.lodges(), 'lodge', )

                self.radioReservesAndOr = andOrRadio()
                ui.space()
                self.selectReserves = selectMulti(reservesOptions(), 'reserve', )

                self.radioMedalsAndOr = andOrRadio()
                ui.space()
                self.selectMedals = selectMulti(medalOptions(), 'medal')

                self.radioAnimalsAndOr = andOrRadio()
                ui.space()
                self.selectAnimals = selectMulti(animalsOptions(), 'animal')

            with ui.row().classes('w-full justify-between items-center'):
                with ui.row():
                    ui.button(text='FILTER', on_click=self.filter_callback)
                    ui.button(text='CLEAR', on_click=self.clear_callback)
                    self.checkboxAllAnimals = ui.checkbox(text='All animals')
                IconUi()

    def updateLodges(self):
        self.selectLodges.set_options(self.db.lodges(), value=None)

    def update_queries_from_filters(self):
        self.queries.updateQuery('lodges', self.selectLodges.value)
        self.queries.updateQuery('reservesAndOr', self.radioReservesAndOr.value)
        self.queries.updateQuery('reserves', self.selectReserves.value)
        self.queries.updateQuery('medalsAndOr', self.radioMedalsAndOr.value)
        self.queries.updateQuery('medals', self.selectMedals.value)
        self.queries.updateQuery('animalsAndOr', self.radioAnimalsAndOr.value)
        self.queries.updateQuery('animals', self.selectAnimals.value)
        self.queries.updateQuery('allAnimals', self.checkboxAllAnimals.value)

    def update_filters_from_preset(self, preset: dict):
        self.selectLodges.set_value(preset['lodges'])
        self.radioReservesAndOr.set_value(preset['reservesAndOr'])
        self.selectReserves.set_value(preset['reserves'])
        self.radioMedalsAndOr.set_value(preset['medalsAndOr'])
        self.selectMedals.set_value(preset['medals'])
        self.radioAnimalsAndOr.set_value(preset['animalsAndOr'])
        self.selectAnimals.set_value(preset['animals'])
        self.checkboxAllAnimals.set_value(preset['allAnimals'])

    def clear_form(self):
        self.selectLodges.set_value('')
        self.radioReservesAndOr.set_value('and')
        self.selectReserves.set_value('')
        self.radioMedalsAndOr.set_value('and')
        self.selectMedals.set_value('')
        self.radioAnimalsAndOr.set_value('and')
        self.selectAnimals.set_value('')
        self.checkboxAllAnimals.set_value('')
        self.checkboxAllAnimals.set_value(False)
