from typing import List

from lib.deca.config import get_save_path
from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from lib.model.trophyanimal import TrophyAnimal


class Db:
    def __init__(self) -> None:
        self._trophyAnimals = loadTrophyAnimals(get_save_path())

    def trophyAnimals(self) ->  List[TrophyAnimal]:
        return self._trophyAnimals

    def lodges(self) ->  List[str]:
        return list(set(map(lambda a: a.lodge, self._trophyAnimals)))

