import bisect
from enum import Enum

from lib.model.constants import DIFFICULTY_SCORE_THRESHOLDS


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
    def getDifficultyName(cls, score):
        scoreIndex = bisect.bisect_right(DIFFICULTY_SCORE_THRESHOLDS, score) - 1

        return str(scoreIndex) + ' - ' + Difficulty(scoreIndex).name.replace('_', ' ')
