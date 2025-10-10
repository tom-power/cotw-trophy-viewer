import os
from pathlib import Path
from typing import List

from lib.db.dbs.animal_medal_db import AnimalMedalDb
from lib.db.dbs.animals_reserves_db import AnimalReserveDb
from lib.db.dbs.preset_db import PresetDb
from lib.db.dbs.trophy_animal_db import TrophyAnimalDb
from lib.db.query.trophy_animal_query import TrophyAnimalQuery
from ..load.loader import Loader
from ..model.trophy_animal import TrophyAnimal


class Db:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path / 'trophy_viewer.db'
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.trophy_animal_db = TrophyAnimalDb(self.db_path)
        self.animal_reserve_db = AnimalReserveDb(self.db_path)
        self.animal_medal_db = AnimalMedalDb(self.db_path)
        self.preset_db = PresetDb(self.db_path)

        self.trophy_animal_query = TrophyAnimalQuery(self.db_path)

    def load(self, loader: Loader):
        self.trophy_animal_db.insert_trophy_animals_dict(loader.load_trophy_animals_dict())
        self.animal_reserve_db.insert_animal_reserves(loader.load_animal_reserves())
        self.animal_medal_db.insert_animal_medals(loader.load_animal_medals())
        self.preset_db.insert_default_presets(loader.load_default_presets())

    def trophyAnimals(self, query: dict | None = None) -> List[TrophyAnimal]:
        return self.trophy_animal_query.trophyAnimals(query)

    def lodges(self) -> dict:
        return self.trophy_animal_query.lodges()

    def presets(self) -> dict:
        return self.preset_db.presets()

    def preset(self, i: int) -> dict:
        return self.preset_db.preset(i)

    def presetAdd(self, name, queryDict):
        return self.preset_db.presetAdd(name, queryDict)

    def presetRemove(self, presetId):
        return self.preset_db.presetRemove(presetId)
