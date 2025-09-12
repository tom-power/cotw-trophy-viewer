from datetime import datetime
from typing import List

import math

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
            "gender": GENDERS[animal.gender] if GENDERS.__contains__(animal.gender) else 'UNKNOWN',
            "weight": round(animal.weight * 100) / 100,
            "rating": math.floor(animal.rating * 100) / 100,
            "badge": animal.badge,
            "difficulty": getDifficultyName(animal.difficulty),
            "difficultyScore": math.floor(animal.difficulty * 1000) / 1000,
            "furType": furTypeName,
            "score": animal.score,
            "datetime": datetime.fromtimestamp(int(animal.datetime)),
        })
    return rows