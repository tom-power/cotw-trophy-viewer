import uuid

from lib.model.animal_type import AnimalType
from lib.model.medal import Medal
from lib.model.reserve import Reserve


class TrophyAnimal:
    def __init__(self, animalType, weight, gender, rating, medal, difficulty, datetime, furType, lodge, reserve):
        self.id = uuid.uuid4()
        self.type: AnimalType = animalType
        self.weight: float = weight
        self.gender: int = gender
        self.rating: float = rating
        self.medal: Medal = medal
        self.difficulty: float = difficulty
        self.datetime = datetime
        self.furType: int = furType
        self.lodge: int = lodge
        self.reserve: Reserve = reserve
