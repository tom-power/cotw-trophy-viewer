from pathlib import Path
from typing import List

from lib.load.trophy_lodge_loader import LoadTrophyLodge
from lib.load.trophy_animal_mapper import TrophyAnimalMapper
from lib.model.trophy_animal import TrophyAnimal


class TrophyAnimalLoader:
    def __init__(self, loadPath: Path):
        self.loadTrophyLodge = LoadTrophyLodge(loadPath=loadPath)
        self.trophyAnimalsMapper = TrophyAnimalMapper()

    def load(self) -> List[TrophyAnimal]:
        lodges = self.loadTrophyLodge.lodges()
        self.trophyAnimalsMapper.add(lodges)
        return self.trophyAnimalsMapper.map()