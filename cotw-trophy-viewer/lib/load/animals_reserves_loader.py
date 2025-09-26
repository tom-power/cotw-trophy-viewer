from lib.model.constants import RESERVES_ANIMALS_CLASSES


class AnimalsReservesLoader:
    @staticmethod
    def load():
        all_animals = []
        for reserve_enum, reserve_dict in RESERVES_ANIMALS_CLASSES.items():
            reserve_index = reserve_enum.value
            for class_level, animals_list in reserve_dict.items():
                for animal_type in animals_list:
                    all_animals.append({'reserve': reserve_index, 'type': animal_type.value})
        return all_animals
