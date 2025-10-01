import os
import sys
from pathlib import Path
from typing import List

from lib.load.loaders.default_presets_loader import DefaultPresetsLoader
from lib.db.dbs.animals_reserves_db import AnimalsReservesDb
from lib.db.dbs.preset_db import PresetDb
from lib.db.dbs.trophy_animal_db import TrophyAnimalDb
from ..load.loader import Loader
from ..model.trophy_animal import TrophyAnimal

TEST_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

if sys.platform == 'win32':
    DB_PATH = Path.home() / 'AppData' / 'Local' / 'cotw-trophy-viewer' / 'data'
else:
    DB_PATH = Path.home() / '.cotw-trophy-viewer' / 'data'

class Db:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path / "trophy_viewer.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.trophy_animal_db = TrophyAnimalDb(self.db_path)
        self.animals_reserves_db = AnimalsReservesDb(self.db_path)
        self.preset_db = PresetDb(self.db_path)

    def load(self, loader: Loader):
        self.trophy_animal_db.load_trophy_animals(loader.load_trophy_animals())
        self.animals_reserves_db.load_animals_reserves(loader.load_animals_reserves())
        self.preset_db.load_presets(loader.load_default_presets())

    def trophyAnimals(self, query: dict | None = None) -> List[TrophyAnimal]:
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
        return self.preset_db.load_presets(DefaultPresetsLoader().load())

    def presetAdd(self, name, queryDict):
        return self.preset_db.presetAdd(name, queryDict)

    def presetRemove(self, presetId):
        return self.preset_db.presetRemove(presetId)
