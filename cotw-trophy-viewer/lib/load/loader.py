from typing import List

from lib.load.loaders.animal_medals_loader import AnimalMedalsLoader
from lib.load.loaders.animals_reserves_loader import AnimalsReservesLoader
from lib.load.loaders.default_presets_loader import DefaultPresetsLoader
from lib.load.loaders.trophy_animal_mapper import TrophyAnimalMapper
from lib.load.loaders.trophy_lodge_loader import LoadTrophyLodge
from lib.model.animal_type_medal import AnimalMedal
from lib.model.animal_type_reserve import AnimalReserve
from lib.model.preset import Preset
from lib.model.trophy_animal import TrophyAnimal
from lib.ui.utils.paths import Paths


class Loader:
    def __init__(self, paths: Paths):
        self.paths = paths
        self._setLoadTrophyLodge()
        self.trophy_animal_mapper = TrophyAnimalMapper()

    def load_trophy_animals_dict(self) -> List[dict]:
        if self.loadFileExists():
            lodges = self.trophy_lodge_loader.lodges()
            self.trophy_animal_mapper.add(lodges)
            return self.trophy_animal_mapper.map_dict()
        return []

    def loadFileExists(self) -> bool:
        return self.paths.getLoadPath() and self.paths.getLoadPath().is_file()

    @staticmethod
    def load_animal_reserves() -> List[AnimalReserve]:
        return AnimalsReservesLoader.load()

    @staticmethod
    def load_animal_medals() -> List[AnimalMedal]:
        return AnimalMedalsLoader.load()

    @staticmethod
    def load_default_presets() -> List[Preset]:
        return DefaultPresetsLoader.load()

    def updateLoadPath(self, new_path):
        self.paths.updateLoadPath(new_path)
        self._setLoadTrophyLodge()

    def resetToDefaultPath(self):
        self.paths.resetToDefaultPath()
        self._setLoadTrophyLodge()


    def _setLoadTrophyLodge(self):
        self.trophy_lodge_loader = LoadTrophyLodge(self.paths.getLoadPath())
