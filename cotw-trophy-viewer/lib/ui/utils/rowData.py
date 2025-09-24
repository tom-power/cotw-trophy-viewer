import math
from datetime import datetime
from typing import List

from lib.model.animalType import AnimalType
from lib.model.constants import GENDERS
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophyanimal import TrophyAnimal
from lib.ui.utils.difficulty import getDifficultyName


def rowData(trophyAnimals: List[TrophyAnimal]) -> List[dict]:
    rows = []

    for animal in trophyAnimals:
        furTypeName = 'UNKNOWN'

        if hasattr(animal, 'furType') and animal.furType is not None:
            furTypeName = animal.furType

        rows.append({
            # 'id': idDisplay,
            'lodge': _naIfNone(animal.lodge, lambda l: f'LODGE {l}'),
            'reserve': _naIfNone(animal.reserve, lambda r: _getReserveName(r)),
            'animal': _naIfNone(animal.type, lambda t: _getAnimalTypeName(t)),
            'gender': _naIfNone(animal.gender, lambda g: GENDERS[g]),
            'weight': _naIfNone(animal.weight, lambda w: round(w * 100) / 100),
            'rating': _naIfNone(animal.rating, lambda r: round(r * 100) / 100),
            'medal': _naIfNone(animal.medal, lambda m: Medal(m).name),
            'difficulty': _naIfNone(animal.difficulty, lambda d: getDifficultyName(d)),
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
