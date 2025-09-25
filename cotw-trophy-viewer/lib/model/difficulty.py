from enum import Enum

from lib.model.constants import DIFFICULTY_SCORE_THRESHOLDS


class Difficulty(Enum):
    TRIVIAL = 0
    MINOR = 1
    VERY_EASY = 2
    EASY = 3
    MEDIUM = 4
    HARD = 5
    VERY_HARD = 6
    MYTHICAL = 7
    LEGENDARY = 8
    FABLED = 9

    @classmethod
    def getDifficultyName(cls, score):
        scoreIndex = -1

        for threshold in DIFFICULTY_SCORE_THRESHOLDS:
            if score >= threshold:
                scoreIndex = scoreIndex + 1
            else:
                break

        return cls(scoreIndex).name
