from pathlib import Path
from typing import List

from lib.load.LoadTrophyLodge import LoadTrophyLodge
from lib.load.TrophyAnimalMapper import TrophyAnimalMapper
from lib.model.trophyanimal import TrophyAnimal


class TrophyAnimalLoader:
    def __init__(self, loadPath: Path):
        self.loadTrophyLodge = LoadTrophyLodge(loadPath=loadPath)
        self.trophyAnimalsMapper = TrophyAnimalMapper()

    def load(self) -> List[TrophyAnimal]:
        lodges = self.loadTrophyLodge.lodges()
        return self.trophyAnimalsMapper.map(lodges)