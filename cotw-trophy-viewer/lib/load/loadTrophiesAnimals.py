from pathlib import Path
from typing import List

from lib.deca.adf import load_adf
from lib.deca.hashes import hash32_func
from lib.model.animalType import AnimalType
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophyanimal import TrophyAnimal


class TrophyAnimalLoader:
    def __init__(self, loadPath: Path):
        self.loadPath = loadPath

    def load(self) -> List[TrophyAnimal]:
        lodges = self._load_trophy_lodges()
        trophy_animals_dict = self._to_trophy_animals_dict(lodges)
        return self._to_trophy_animal_list(trophy_animals_dict)

    def _load_trophy_lodges(self) -> dict:
        if self.loadPath is None:
            return {}
        adf = load_adf(self.loadPath / "trophy_lodges_adf", verbose=True).adf
        return adf.table_instance_values[0]

    @staticmethod
    def _to_trophy_animals_dict(trophyLodge: dict) -> List[dict]:
        return TrophyAnimalLoader.fromTrophyAnimals(trophyLodge) + TrophyAnimalLoader.fromTrophyHybrids(trophyLodge)

    @staticmethod
    def fromTrophyAnimals(trophyLodge: dict) -> list[dict]:
        trophy_animals = []
        if "TrophyAnimals" in trophyLodge and "Trophies" in trophyLodge["TrophyAnimals"]:
            trophies = trophyLodge["TrophyAnimals"]["Trophies"]
            for trophy in trophies:
                if "TrophyAnimal" in trophy and trophy["LodgeId"] != 0:
                    trophyAnimal = trophy["TrophyAnimal"]
                    trophyAnimal['LodgeId'] = trophy["LodgeId"]
                    trophy_animals.append(trophyAnimal)
        return trophy_animals

    @staticmethod
    def fromTrophyHybrids(trophyLodge: dict) -> list[dict]:
        trophy_animals = []
        if "TrophyHybrids" in trophyLodge and "Trophies" in trophyLodge["TrophyHybrids"]:
            trophies = trophyLodge["TrophyHybrids"]["Trophies"]
            for trophy in trophies:
                if "TrophyHybrid" in trophy and "TrophyAnimals" in trophy["TrophyHybrid"]:
                    trophyAnimals = trophy["TrophyHybrid"]["TrophyAnimals"]
                    for trophyAnimal in trophyAnimals:
                        trophyAnimal['LodgeId'] = trophy["LodgeId"]
                        trophy_animals.append(trophyAnimal)
        return trophy_animals

    def _to_trophy_animal_list(self, trophiesAnimalsDict: List[dict]) -> List[TrophyAnimal]:
        trophiesAnimals = []
        for animal_data in trophiesAnimalsDict:
            animal = TrophyAnimal(
                animalType=(self._find_animal_type(animal_data.get("Type", 0))),
                weight=(animal_data.get("Weight", 0.0)),
                gender=(animal_data.get("IsMale", 0)),
                rating=(animal_data.get("TrophyScore", 0.0)),
                medal=Medal(animal_data.get("ScoreRank", 0)),
                difficulty=(animal_data.get("Difficulty", 0.0)),
                datetime=(str(animal_data.get("HarvestedAt", 0))),
                furType=(animal_data.get("VariationIndex", 0)),
                reserve=(Reserve(animal_data.get("HarvestReserve", 0))),
                lodge=(animal_data.get("LodgeId", 0)),
            )
            trophiesAnimals.append(animal)
        return trophiesAnimals

    def _find_animal_type(self, trophyAnimalType) -> AnimalType | None:
        for a in AnimalType:
            if trophyAnimalType == hash32_func(a.name.lower()):
                return a
        return None