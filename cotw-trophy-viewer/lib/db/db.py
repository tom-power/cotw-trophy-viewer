from typing import List

from littletable import Table

from lib.deca.config import get_save_path
from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from lib.model.trophyanimal import TrophyAnimal


class Db:
    def __init__(self) -> None:
        self._trophyAnimals = Table('TrophyAnimals')
        self._trophyAnimals.insert_many(loadTrophyAnimals(get_save_path()))

    def trophyAnimals(self, lodges, reserves, animals) -> List[TrophyAnimal]:
        if len(lodges) > 0 or len(reserves) > 0 or len(animals) > 0:
            lodgeSelection = self._trophyAnimals.where(lodge=Table.is_in(lodges))
            reserveSelection = self._trophyAnimals.where(reserve=Table.is_in(reserves))
            animalsSelection = self._trophyAnimals.where(type=Table.is_in(animals))
            return list(
                lodgeSelection
                    .outer_join(Table.FULL_OUTER_JOIN, reserveSelection, id="id")
                    .outer_join(Table.FULL_OUTER_JOIN, animalsSelection, id="id")
            )
        return list(self._trophyAnimals)

    def lodges(self) -> List[str]:
        return list(set(map(lambda a: a.lodge, self._trophyAnimals)))

