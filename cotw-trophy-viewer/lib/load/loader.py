from pathlib import Path
from typing import List

from lib.load.loaders.animals_reserves_loader import AnimalsReservesLoader
from lib.load.loaders.default_presets_loader import DefaultPresetsLoader
from lib.load.loaders.trophy_animal_mapper import TrophyAnimalMapper
from lib.load.loaders.trophy_lodge_loader import LoadTrophyLodge
from lib.model.animal_reserve import AnimalReserve
from lib.model.preset import Preset
from lib.model.trophy_animal import TrophyAnimal


class Loader:
    def __init__(self, loadPath: Path):
        self.loadPath = loadPath
        self.trophy_lodge_loader = LoadTrophyLodge(loadPath)
        self.trophy_animal_mapper = TrophyAnimalMapper()

    @staticmethod
    def load_animals_reserves() -> List[AnimalReserve]:
        return AnimalsReservesLoader.load()

    @staticmethod
    def load_default_presets() -> List[Preset]:
        return DefaultPresetsLoader.load()

    def load_trophy_animals(self) -> List[TrophyAnimal]:
        lodges = self.trophy_lodge_loader.lodges()
        self.trophy_animal_mapper.add(lodges)
        return self.trophy_animal_mapper.map()
