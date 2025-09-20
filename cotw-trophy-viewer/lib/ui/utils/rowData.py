import math
from datetime import datetime
from typing import List

from lib.model.constants import RESERVES, GENDERS
from lib.ui.utils.ratings import getDifficultyName


def rowData(trophyAnimals) -> List[dict]:
    rows = []

    for animal in trophyAnimals:
        furTypeName = "UNKNOWN"

        if hasattr(animal, "furType") and animal.furType is not None:
            furTypeName = animal.furType

        rows.append({
            # "id": idDisplay,
            "lodge": animal.lodge,
            "reserve": list(RESERVES[animal.reserve].keys())[0] if RESERVES.__contains__(
                animal.reserve) else 'UNKNOWN',
            "animal": animal.type,
            "gender": _naIfNone(animal.gender, lambda g: GENDERS[g]),
            "weight": _naIfNone(animal.weight, lambda w: round(w * 100) / 100),
            "rating": _naIfNone(animal.rating, lambda r: math.floor(r * 100) / 100),
            "badge": _naIfNone(animal.badge),
            "difficulty": _naIfNone(animal.difficulty, lambda d: getDifficultyName(d)),
            "difficultyScore": _naIfNone(animal.difficulty, lambda d: math.floor(d * 1000) / 1000),
            "furType": _naIfNone(furTypeName),
            "score": _naIfNone(animal.score),
            "datetime": _naIfNone(animal.datetime, lambda d: datetime.fromtimestamp(int(d))),
        })
    return rows


def _naIfNone(value, fn=lambda a: a):
    if value is None:
        return 'NA'
    return fn(value),
