from pathlib import Path
from typing import List

from lib.deca.adf import load_adf
from lib.deca.hashes import hash32_func
from lib.model.animal_type import AnimalType
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophy_animal import TrophyAnimal


class LoadTrophyLodge:
    def __init__(self, loadPath: Path):
        self.loadPath = loadPath

    def lodges(self) -> dict:
        return self._load_trophy_lodges()

    def _load_trophy_lodges(self) -> dict:
        if self.loadPath is None:
            return {}
        adf = load_adf(self.loadPath / "trophy_lodges_adf", verbose=True).adf
        return adf.table_instance_values[0]
