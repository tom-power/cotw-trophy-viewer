import os
import sys
from pathlib import Path

from numba.cpython.new_mathimpl import DBL_MAX

from lib.load.animals_reserves_loader import AnimalsReservesLoader
from lib.load.default_presets_loader import DefaultPresetsLoader
from lib.load.trophy_animal_loader import TrophyAnimalLoader
from .animals_reserves_db import AnimalsReservesDb
from .preset_db import PresetDb
from .trophy_animal_db import TrophyAnimalDb

TEST_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

if sys.platform == 'win32':
    DB_PATH = Path.home() / 'AppData' / 'Local' / 'cotw-trophy-viewer' / 'data'
else:
    DB_PATH = Path.home() / '.cotw-trophy-viewer' / 'data'

class Db:
    def __init__(self, loadPath: Path, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path / "trophy_viewer.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.trophy_animal_db = TrophyAnimalDb(self.db_path)
        self.animals_reserves_db = AnimalsReservesDb(self.db_path)
        self.preset_db = PresetDb(self.db_path)

        self.trophy_animal_loader = TrophyAnimalLoader(loadPath)
        self.animals_reserves_loader = AnimalsReservesLoader()
        self.default_presets_loader = DefaultPresetsLoader()

        self.trophy_animal_db.insert_trophy_animals(self.trophy_animal_loader.load())
        self.animals_reserves_db.insert_animals_reserves(self.animals_reserves_loader.load())
        self.preset_db.init_presets(self.default_presets_loader.load())


    def trophyAnimals(self, query: dict | None = None):
        return self.trophy_animal_db.trophyAnimals(query)

    def lodges(self) -> dict:
        return self.trophy_animal_db.lodges()

    def presets(self) -> dict:
        return self.preset_db.presets()

    def preset(self, i: int) -> dict:
        return self.preset_db.preset(i)

    def presetsClear(self):
        return self.preset_db.presetsClear()

    def presetInit(self):
        return self.preset_db.init_presets(DefaultPresetsLoader().load())

    def presetAdd(self, name, queryDict):
        return self.preset_db.presetAdd(name, queryDict)

    def presetRemove(self, presetId):
        return self.preset_db.presetRemove(presetId)