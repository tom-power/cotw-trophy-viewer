import math
from datetime import datetime
from typing import List

from lib.model.animal_type import AnimalType
from lib.model.difficulty import Difficulty
from lib.model.gender import Gender
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophy_animal import TrophyAnimal


def rowData(trophyAnimals: List[TrophyAnimal]) -> List[dict]:
    rows = []

    for animal in trophyAnimals:
        furTypeName = 'UNKNOWN'

        if hasattr(animal, 'furType') and animal.furType is not None:
            furTypeName = animal.furType

        rows.append({
            # 'id': idDisplay,
            'lodge': _naIfNone(animal.lodge, lambda l: f'LODGE {l.lodgeId}'),
            'reserve': _naIfNone(animal.reserve, lambda r: _getReserveName(r)),
            'animal': _naIfNone(animal.type, lambda t: _getAnimalTypeName(t)),
            'gender': _naIfNone(animal.gender, lambda g: Gender(g).name),
            'weight': _naIfNone(animal.weight, lambda w: round(w * 100) / 100),
            'rating': _naIfNone(animal.rating, lambda r: round(r * 100) / 100),
            'medal': _naIfNone(animal.medal, lambda m: Medal(m).name),
            'difficulty': _naIfNone(animal.difficulty, lambda d: Difficulty.getDifficultyName(d)),
            'difficultyScore': _naIfNone(animal.difficulty, lambda d: math.floor(d * 1000) / 1000),
            'furType': _naIfNone(furTypeName),
            'datetime': _naIfNone(animal.datetime, lambda d: datetime.fromtimestamp(int(d)).strftime(
                "%d/%m/%y %H:%M"))
            ,
        })
    return rows


def _getReserveName(reserve) -> str:
    return Reserve(reserve).reserveName()


def _getAnimalTypeName(key: int) -> str:
    try:
        animal_type = AnimalType(key)
        return animal_type.animalName()
    except ValueError:
        return f'{key}'


def _naIfNone(value, fn=lambda a: a):
    if value is None:
        return 'NA'
    return fn(value)
