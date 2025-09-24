from pathlib import Path
from typing import List

from lib.deca.adf import load_adf
from lib.deca.hashes import hash32_func
from lib.model.animalType import AnimalType
from lib.model.trophyanimal import TrophyAnimal


def loadTrophyAnimals(loadPath: Path) -> List[TrophyAnimal]:
    def _loadTrophyLodges() -> dict:
        if loadPath is None:
            return {}
        adf = load_adf(loadPath / "trophy_lodges_adf", verbose=True).adf
        return adf.table_instance_values[0]

    def _toTrophyAnimalsDict(trophyLodge: dict) -> List[dict]:
        trophy_animals = []
        if "TrophyAnimals" in trophyLodge and "Trophies" in trophyLodge["TrophyAnimals"]:
            trophies = trophyLodge["TrophyAnimals"]["Trophies"]
            for trophy in trophies:
                if "TrophyAnimal" in trophy:
                    trophyAnimal = trophy["TrophyAnimal"]
                    trophyAnimal['LodgeId'] = trophy["LodgeId"]
                    trophy_animals.append(trophyAnimal)
        return trophy_animals

    def _toTrophyAnimalList(trophiesAnimalsDict: List[dict]) -> List[TrophyAnimal]:
        trophiesAnimals = []
        for animal_data in trophiesAnimalsDict:
            animal = TrophyAnimal(
                animalType=(_find_animal_type(animal_data.get("Type", 0))),
                weight=(animal_data.get("Weight", 0.0)),
                gender=(animal_data.get("IsMale", 0)),
                rating=(animal_data.get("TrophyScore", 0.0)),
                medal=(animal_data.get("ScoreRank", 0)),
                difficulty=(animal_data.get("Difficulty", 0.0)),
                datetime=(str(animal_data.get("HarvestedAt", 0))),
                furType=(animal_data.get("VariationIndex", 0)),
                reserve=(animal_data.get("HarvestReserve", 0)),
                lodge=(animal_data.get("LodgeId", 0) + 1),
            )
            trophiesAnimals.append(animal)
        return trophiesAnimals

    lodges = _loadTrophyLodges()
    trophyAnimalsDict = _toTrophyAnimalsDict(lodges)
    return _toTrophyAnimalList(trophyAnimalsDict)


def _find_animal_type(trophyAnimalType) -> AnimalType | None:
    for a in AnimalType:
        if trophyAnimalType == hash32_func(a.name.lower()):
            return a
    return None
