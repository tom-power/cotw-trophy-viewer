from pathlib import Path
from typing import List

from lib.load.LoadTrophyAnimals import LoadTrophyAnimals
from lib.model.trophyanimal import TrophyAnimal


def loadTrophyAnimals(loadPath: Path) -> List[TrophyAnimal]:
    return LoadTrophyAnimals(loadPath).__call__()
