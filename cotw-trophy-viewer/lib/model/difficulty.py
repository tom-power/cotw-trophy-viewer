import bisect
from enum import Enum

class Difficulty(Enum):
    TRIVIAL = 1
    MINOR = 2
    VERY_EASY = 3
    EASY = 4
    MEDIUM = 5
    HARD = 6
    VERY_HARD = 7
    MYTHICAL = 8
    LEGENDARY = 9
    FABLED = 10

    @classmethod
    def getDifficultyName(cls, score) -> str:
        scoreIndex = bisect.bisect_right(DIFFICULTY_SCORE_THRESHOLDS, score)

        return str(scoreIndex) + ' - ' + Difficulty(scoreIndex).name.replace('_', ' ')

DIFFICULTY_SCORE_THRESHOLDS = [0, 0.115, 0.225, 0.335, 0.445, 0.555, 0.665, 0.775, 0.885, 0.995]
