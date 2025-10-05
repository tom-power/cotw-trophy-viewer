from lib.model.animal_type import AnimalType
from lib.model.reserve import Reserve


class AnimalReserve:
    def __init__(self, animalType: AnimalType, reserve: Reserve):
        self.type = animalType
        self.reserve = reserve

