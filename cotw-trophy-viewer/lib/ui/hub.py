from typing import List

from lib.load.loader import Loader
from lib.db.db import Db
from lib.model.trophy_animal import TrophyAnimal

class Hub:
    def __init__(self, db: Db, loader: Loader) -> None:
        self.db = db
        self.loader = loader
        self.db.insert_trophy_animals(self.loader.load_trophy_animals())
        self.db.insert_animals_reserves(self.loader.load_animals_reserves())
        self.db.insert_presets(self.loader.load_default_presets())


    def trophyAnimals(self, query: dict | None = None) -> List[TrophyAnimal]:
        return self.db.trophyAnimals(query)

    def lodges(self) -> dict:
        return self.db.lodges()

    def presets(self) -> dict:
        return self.db.presets()

    def preset(self, i: int) -> dict:
        return self.db.preset(i)

    def presetAdd(self, name, queryDict):
        return self.db.presetAdd(name, queryDict)

    def presetRemove(self, presetId):
        return self.db.presetRemove(presetId)