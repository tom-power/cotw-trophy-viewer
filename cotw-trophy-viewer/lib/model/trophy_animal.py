import uuid

from lib.model.animal_type import AnimalType
from lib.model.lodge import Lodge
from lib.model.medal import Medal
from lib.model.reserve import Reserve


class TrophyAnimal:
    def __init__(self, animalType: AnimalType, weight, gender, rating, medal, difficulty, datetime, furType,
                 slotId, lodge: Lodge, reserve: Reserve):
        self.id = uuid.uuid4()
        self.type: AnimalType = animalType
        self.weight: float = weight
        self.gender: int = gender
        self.rating: float = rating
        self.medal: Medal = medal
        self.difficulty: float = difficulty
        self.datetime = datetime
        self.furType: int = furType
        self.slotId: int = slotId
        self.lodge: Lodge = lodge
        self.reserve: Reserve = reserve
