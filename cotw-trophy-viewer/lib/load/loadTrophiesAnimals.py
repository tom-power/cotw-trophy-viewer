from pathlib import Path
from typing import List

from lib.load.LoadTrophyAnimals import LoadTrophyAnimals
from lib.load.mapAnimalTypesNames import getMapAnimalTypeNames
from lib.load.mapAnimalTypesNames import getMapAnimalTypeNames
from lib.model.trophyanimal import TrophyAnimal


def loadTrophyAnimals(loadPath: Path) -> List[TrophyAnimal]:
    return LoadTrophyAnimals(loadPath, getMapAnimalTypeNames()).__call__()
