from pathlib import Path
from typing import List

from lib.load.LoadTrophyAnimals import LoadTrophyAnimals
from lib.load.mapAnimalTypes import getMapAnimalTypes
from lib.model.trophyanimal import TrophyAnimal


def loadTrophyAnimals(loadPath: Path) -> List[TrophyAnimal]:
    return LoadTrophyAnimals(loadPath, getMapAnimalTypes()).__call__()
