from typing import List

from lib.model.animal_type_medal import AnimalMedal
from lib.model.medals_animals import MEDALS_ANIMALS


class AnimalMedalsLoad:
    @staticmethod
    def load() -> List[AnimalMedal]:
        animal_medals = []
        for medal_enum, medal_list in MEDALS_ANIMALS.items():
            for animal_type in medal_list:
                animal_medal = AnimalMedal(
                    animalType=animal_type,
                    medal=medal_enum
                )
                animal_medals.append(animal_medal)
        return animal_medals
