from lib.model.animal_type import AnimalType
from lib.model.medal import Medal

class AnimalFur:
    def __init__(self, animalType: AnimalType, furId: int, furName: str):
        self.type = animalType
        self.furId = furId
        self.furName = furName

