import os
import sys
from pathlib import Path

from lib.load.animals_reserves_loader import AnimalsReservesLoader
from lib.load.default_presets_loader import DefaultPresetsLoader
from lib.load.TrophyAnimalLoader import TrophyAnimalLoader
from .animals_reserves_manager import AnimalsReservesManager
from .preset_manager import PresetManager
from .trophy_animal_manager import TrophyAnimalManager

TEST_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

if sys.platform == 'win32':
    DB_PATH = Path.home() / 'AppData' / 'Local' / 'cotw-trophy-viewer' / 'data'
else:
    DB_PATH = Path.home() / '.cotw-trophy-viewer' / 'data'

class Db:
    def __init__(self, loadPath: Path, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path / "trophy_viewer.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.trophy_animal_manager = TrophyAnimalManager(self.db_path)
        self.trophy_animal_manager.insert_trophy_animals(TrophyAnimalLoader(loadPath).load())

        self.animals_reserves_manager = AnimalsReservesManager(self.db_path)
        self.animals_reserves_manager.insert_animals_reserves(AnimalsReservesLoader().load())

        self.preset_manager = PresetManager(self.db_path)
        self.preset_manager.presetInit(DefaultPresetsLoader().load())


    def trophyAnimals(self, query: dict | None = None):
        return self.trophy_animal_manager.trophyAnimals(query)

    def lodges(self) -> dict:
        return self.trophy_animal_manager.lodges()

    def presets(self):
        return self.preset_manager.presets()

    def preset(self, i: int) -> dict:
        return self.preset_manager.preset(i)

    def presetsClear(self):
        return self.preset_manager.presetsClear()

    def presetInit(self):
        return self.preset_manager.presetInit(DefaultPresetsLoader().load())

    def presetAdd(self, name, queryDict):
        return self.preset_manager.presetAdd(name, queryDict)

    def presetRemove(self, presetId):
        return self.preset_manager.presetRemove(presetId)