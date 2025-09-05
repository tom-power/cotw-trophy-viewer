from typing import Callable

from lib.model.animalType import AnimalType


def getMapAnimalTypes() -> Callable[[int], str]:
    def mapAnimalTypes(trophyAnimalType: int) -> str:
        try:
            return AnimalType(trophyAnimalType).animalName()
        except:
            return str(trophyAnimalType)

    return mapAnimalTypes