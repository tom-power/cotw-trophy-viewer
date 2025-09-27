from pathlib import Path
from typing import List

from lib.deca.adf import load_adf
from lib.deca.hashes import hash32_func
from lib.model.animal_type import AnimalType
from lib.model.lodge import Lodge
from lib.model.lodge_type import LodgeType
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophy_animal import TrophyAnimal


class TrophyAnimalMapper:
    def __init__(self):
        self.trophyLodges = None
        self.lodge_map = {}

    def add(self, trophyLodges: dict):
        self.trophyLodges = trophyLodges

    def map(self) -> List[TrophyAnimal]:
        self._map_lodges()
        trophy_animals_dict = self._to_trophy_animals_dict()
        return self._to_trophy_animal_list(trophy_animals_dict)

    def _map_lodges(self):
        if "TrophyLodges" in self.trophyLodges and "Lodges" in self.trophyLodges["TrophyLodges"]:
            lodges = self.trophyLodges["TrophyLodges"]["Lodges"]
            for lodge in lodges:
                if "Id" in lodge and "Type" in lodge and "TypeId" in lodge:
                    self.lodge_map[lodge["Id"]] = Lodge(lodge["Id"], LodgeType(lodge["Type"]), lodge["TypeId"])

    def _to_trophy_animals_dict(self) -> List[dict]:
        return self._fromTrophyAnimals() + self._fromTrophyHybrids()

    def _fromTrophyAnimals(self) -> list[dict]:
        trophy_animals = []
        if "TrophyAnimals" in self.trophyLodges and "Trophies" in self.trophyLodges["TrophyAnimals"]:
            trophies = self.trophyLodges["TrophyAnimals"]["Trophies"]
            for trophy in trophies:
                if "TrophyAnimal" in trophy and trophy["LodgeId"] != 0:
                    trophyAnimal = trophy["TrophyAnimal"]
                    trophyAnimal['LodgeId'] = trophy["LodgeId"]
                    trophy_animals.append(trophyAnimal)
        return trophy_animals

    def _fromTrophyHybrids(self) -> list[dict]:
        trophy_animals = []
        if "TrophyHybrids" in self.trophyLodges and "Trophies" in self.trophyLodges["TrophyHybrids"]:
            trophies = self.trophyLodges["TrophyHybrids"]["Trophies"]
            for trophy in trophies:
                if "TrophyHybrid" in trophy and "TrophyAnimals" in trophy["TrophyHybrid"]:
                    trophyAnimals = trophy["TrophyHybrid"]["TrophyAnimals"]
                    for trophyAnimal in trophyAnimals:
                        if trophy["LodgeId"] != 0:
                            trophyAnimal['LodgeId'] = trophy["LodgeId"]
                            trophy_animals.append(trophyAnimal)
        return trophy_animals

    def _to_trophy_animal_list(self, trophiesAnimalsDict: List[dict]) -> List[TrophyAnimal]:
        trophiesAnimals = []
        for animal_data in trophiesAnimalsDict:
            lodge_id = animal_data.get("LodgeId")
            lodge = self.lodge_map.get(lodge_id)

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
                lodge=lodge if lodge_id else None,
            )
            trophiesAnimals.append(animal)
        return trophiesAnimals

    @staticmethod
    def _find_animal_type(trophyAnimalType) -> AnimalType | None:
        for a in AnimalType:
            if trophyAnimalType == hash32_func(a.name.lower()):
                return a
        return None