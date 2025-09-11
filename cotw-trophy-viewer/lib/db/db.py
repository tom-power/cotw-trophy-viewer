from typing import List

from littletable import Table

from lib.deca.config import get_save_path
from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from lib.model.trophyanimal import TrophyAnimal


class Db:
    def __init__(self) -> None:
        self._trophyAnimals = Table('TrophyAnimals')
        self._trophyAnimals.insert_many(loadTrophyAnimals(get_save_path()))

    def trophyAnimals(self, query: dict) -> List[TrophyAnimal]:
        _lodges = query['lodges']
        _reserves = query['reserves']
        _badges = query['badges']
        _animals = query['animals']

        table=self._trophyAnimals

        if len(_lodges) > 0 or len(_reserves) > 0 or len(_animals) > 0:
            lodgeSelection = self._trophyAnimals.where(lodge=Table.is_in(_lodges))
            reserveSelection = self._trophyAnimals.where(reserve=Table.is_in(_reserves))
            badgeSelection = self._trophyAnimals.where(badge=Table.is_in(_badges))
            animalsSelection = self._trophyAnimals.where(type=Table.is_in(_animals))
            table = (lodgeSelection
                    .outer_join(Table.FULL_OUTER_JOIN, lodgeSelection, id="id")
                    .outer_join(Table.FULL_OUTER_JOIN, reserveSelection, id="id")
                    .outer_join(Table.FULL_OUTER_JOIN, badgeSelection, id="id")
                    .outer_join(Table.FULL_OUTER_JOIN, animalsSelection, id="id"))

        return list(table)

    def lodges(self) -> List[str]:
        return list(set(map(lambda a: a.lodge, self._trophyAnimals)))

