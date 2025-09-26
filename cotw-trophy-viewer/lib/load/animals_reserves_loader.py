from typing import List

from lib.model.animalReserve import AnimalReserve
from lib.model.constants import RESERVES_ANIMALS_CLASSES


class AnimalsReservesLoader:
    @staticmethod
    def load() -> List[AnimalReserve]:
        all_animals = []
        for reserve_enum, reserve_dict in RESERVES_ANIMALS_CLASSES.items():
            for class_level, animals_list in reserve_dict.items():
                for animal_type in animals_list:
                    animal_reserve = AnimalReserve(
                        animalType=animal_type,
                        reserve=reserve_enum
                    )
                    all_animals.append(animal_reserve)
        return all_animals
