from typing import List

from lib.load.model.animal_medals_loader import AnimalMedalsLoad
from lib.load.model.animals_reserves_loader import AnimalsReservesLoad
from lib.load.model.presets_loader import PresetsLoad
from lib.load.trophy_lodge.lodge_mapper import LodgeMapper
from lib.load.trophy_lodge.trophy_animal_mapper import TrophyAnimalMapper
from lib.load.trophy_lodge.trophy_lodge_loader import LoadTrophyLodge
from lib.model.animal_type_medal import AnimalMedal
from lib.model.animal_type_reserve import AnimalReserve
from lib.model.preset import Preset
from lib.ui.utils.paths import Paths


class Loader:
    def __init__(self, paths: Paths):
        self.paths = paths
        self._setLoadTrophyLodge()
        self.trophy_animal_mapper = TrophyAnimalMapper()
        self.lodge_mapper = LodgeMapper()

    def load_trophy_animals(self) -> List[dict]:
        if self.loadFileExists():
            lodges = self.trophy_lodge_loader.lodges()
            self.trophy_animal_mapper.add(lodges)
            return self.trophy_animal_mapper.map()
        return []

    def load_lodges(self) -> List[dict]:
        if self.loadFileExists():
            lodges = self.trophy_lodge_loader.lodges()
            self.lodge_mapper.add(lodges)
            return self.lodge_mapper.map()
        return []

    def loadFileExists(self) -> bool:
        return self.paths.getLoadPath() and self.paths.getLoadPath().is_file()

    def updateLoadPath(self, new_path):
        self.paths.updateLoadPath(new_path)
        self._setLoadTrophyLodge()

    def resetToDefaultPath(self):
        self.paths.resetToDefaultPath()
        self._setLoadTrophyLodge()

    def _setLoadTrophyLodge(self):
        self.trophy_lodge_loader = LoadTrophyLodge(self.paths.getLoadPath())

    @staticmethod
    def load_animal_reserves() -> List[AnimalReserve]:
        return AnimalsReservesLoad.load()

    @staticmethod
    def load_animal_medals() -> List[AnimalMedal]:
        return AnimalMedalsLoad.load()

    @staticmethod
    def load_presets() -> List[Preset]:
        return PresetsLoad.load()
