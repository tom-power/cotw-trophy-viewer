import os
import sys
from pathlib import Path
from typing import List

from lib.load.loaders.default_presets_loader import DefaultPresetsLoader
from lib.db.dbs.animals_reserves_db import AnimalsReservesDb
from lib.db.dbs.preset_db import PresetDb
from lib.db.dbs.trophy_animal_db import TrophyAnimalDb
from ..model.animal_reserve import AnimalReserve
from ..model.preset import Preset
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


    def insert_trophy_animals(self, trophy_animals: List[TrophyAnimal]) -> None:
        self.trophy_animal_db.insert_trophy_animals(trophy_animals)


    def insert_animals_reserves(self, animals_reserves: List[AnimalReserve]):
        self.animals_reserves_db.insert_animals_reserves(animals_reserves)

    def insert_presets(self, default_presets: List[Preset]):
        self.preset_db.insert_presets(default_presets)

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
        return self.preset_db.insert_presets(DefaultPresetsLoader().load())

    def presetAdd(self, name, queryDict):
        return self.preset_db.presetAdd(name, queryDict)

    def presetRemove(self, presetId):
        return self.preset_db.presetRemove(presetId)
