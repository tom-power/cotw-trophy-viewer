from lib.model.animal_type import AnimalType
from lib.model.medal import Medal


class AnimalMedal:
    def __init__(self, animalType: AnimalType, medal: Medal):
        self.type = animalType
        self.medal = medal

