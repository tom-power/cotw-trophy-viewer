from typing import Callable

from lib.deca.hashes import hash32_func
from lib.model.animalType import AnimalType

def mapAnimalTypeName(trophyAnimalType: int) -> str:
    animalType = _find_animal_type(trophyAnimalType)
    if animalType is not None:
        return animalType.animalName()
    else:
        return str(trophyAnimalType)

def _find_animal_type(trophyAnimalType) -> AnimalType | None:
    for a in AnimalType:
        if trophyAnimalType == hash32_func(a.name.lower()):
            return a
    return None
