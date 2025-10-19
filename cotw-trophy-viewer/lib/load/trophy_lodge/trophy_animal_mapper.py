from typing import List


class TrophyAnimalMapper:
    def __init__(self):
        self.trophyLodges = None

    def add(self, trophyLodges: dict):
        self.trophyLodges = trophyLodges

    def map(self) -> List[dict]:
        trophy_animals_from_lodges = self._trophy_animals_from_lodges()
        return self._to_trophy_animals_dict(trophy_animals_from_lodges)

    def _trophy_animals_from_lodges(self) -> List[dict]:
        return self._fromLodgesTrophyAnimals() + self._fromLodgesTrophyHybrids()

    def _fromLodgesTrophyAnimals(self) -> list[dict]:
        trophy_animals = []
        if "TrophyAnimals" in self.trophyLodges and "Trophies" in self.trophyLodges["TrophyAnimals"]:
            trophies = self.trophyLodges["TrophyAnimals"]["Trophies"]
            for trophy in trophies:
                if "TrophyAnimal" in trophy and trophy["LodgeId"] != 0:
                    trophyAnimal = trophy["TrophyAnimal"]
                    trophyAnimal['LodgeId'] = trophy["LodgeId"]
                    trophyAnimal['SlotId'] = trophy["SlotId"]
                    trophy_animals.append(trophyAnimal)
        return trophy_animals

    def _fromLodgesTrophyHybrids(self) -> list[dict]:
        trophy_animals = []
        if "TrophyHybrids" in self.trophyLodges and "Trophies" in self.trophyLodges["TrophyHybrids"]:
            trophies = self.trophyLodges["TrophyHybrids"]["Trophies"]
            for trophy in trophies:
                if "TrophyHybrid" in trophy and "TrophyAnimals" in trophy["TrophyHybrid"]:
                    trophyAnimals = trophy["TrophyHybrid"]["TrophyAnimals"]
                    for trophyAnimal in trophyAnimals:
                        if trophy["LodgeId"] != 0:
                            trophyAnimal['LodgeId'] = trophy["LodgeId"]
                            trophyAnimal['SlotId'] = trophy["SlotId"]
                            trophy_animals.append(trophyAnimal)
        return trophy_animals


    def _to_trophy_animals_dict(self, trophiesAnimalsDict: List[dict]) -> List[dict]:
        trophiesAnimals = []
        for animal_data in trophiesAnimalsDict:
            animal = {
                "typeId": (animal_data.get("Type", 0)),
                "weight": animal_data.get("Weight", 0.0),
                "gender": animal_data.get("IsMale", 0),
                "rating": animal_data.get("TrophyScore", 0.0),
                "medalId": animal_data.get("ScoreRank", 0),
                "difficulty": animal_data.get("Difficulty", 0.0),
                "datetime": str(animal_data.get("HarvestedAt", 0)),
                "furType": animal_data.get("VariationIndex", 0),
                "reserveId": animal_data.get("HarvestReserve", 0),
                "lodgeId": animal_data.get("LodgeId"),
                "slotId": animal_data.get("SlotId"),
            }
            trophiesAnimals.append(animal)
        return trophiesAnimals
