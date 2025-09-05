from pathlib import Path
from typing import Callable, List

from lib.deca.adf import load_adf
from lib.model.trophyanimal import TrophyAnimal


class LoadTrophyAnimals:
    def __init__(self, loadPath: Path, mapAnimalTypes: Callable[[int], str] = lambda s: s):
        self.loadPath = loadPath
        self.mapAnimalTypes = mapAnimalTypes

    def __call__(self, *args, **kwargs) -> List[TrophyAnimal]:
        lodges = self._loadTrophyLodges()
        trophyAnimalsDict = self._toTrophyAnimalsDict(lodges)
        return self._toTrophyAnimalList(trophyAnimalsDict)

    TROPHY_LODGES_FILE = "trophy_lodges_adf"

    def _loadTrophyLodges(self) -> dict:
        adf = load_adf(self.loadPath / self.TROPHY_LODGES_FILE, verbose=True).adf
        return adf.table_instance_values[0]

    @staticmethod
    def _toTrophyAnimalsDict(trophyLodge: dict) -> List[dict]:
        trophy_animals = []

        if "TrophyAnimals" in trophyLodge and "Trophies" in trophyLodge["TrophyAnimals"]:
            trophies = trophyLodge["TrophyAnimals"]["Trophies"]
            for trophy in trophies:
                if "TrophyAnimal" in trophy:
                    trophy_animals.append(trophy["TrophyAnimal"])

        return trophy_animals

    def _toTrophyAnimalList(self, trophiesAnimalsDict: List[dict]) -> List[
        TrophyAnimal]:
        trophiesAnimals = []

        for animal_data in trophiesAnimalsDict:
            weight = animal_data.get("Weight", 0.0)
            gender = animal_data.get("IsMale", 0)
            score = animal_data.get("TrophyScore", 0.0)
            rating = animal_data.get("ScoreRank", 0)
            difficulty = animal_data.get("Difficulty", 0.0)
            datetime = str(animal_data.get("HarvestedAt", 0))
            fur_type = animal_data.get("VariationIndex", 0)
            animal_type = self.mapAnimalTypes(animal_data.get("Type", 0))
            animal = TrophyAnimal(
                type=animal_type,
                weight=weight,
                gender=gender,
                score=score,
                rating=rating,
                difficulty=difficulty,
                datetime=datetime,
                furType=fur_type
            )

            trophiesAnimals.append(animal)

        return trophiesAnimals
