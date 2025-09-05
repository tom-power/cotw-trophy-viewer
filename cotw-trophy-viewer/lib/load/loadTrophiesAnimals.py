from pathlib import Path
from typing import List

from lib.load.LoadTrophyAnimals import LoadTrophyAnimals
from lib.load.mapAnimalTypes import getMapAnimalTypes
from lib.model.trophyanimal import TrophyAnimal


def loadTrophyAnimals(savePath: Path) -> List[TrophyAnimal]:
    return LoadTrophyAnimals(savePath, getMapAnimalTypes()).__call__()
