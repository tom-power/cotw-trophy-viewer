from lib.model.animal_type import AnimalType


def animalName(animalType: AnimalType) -> str:
    return animalType.name.replace("_", " ")