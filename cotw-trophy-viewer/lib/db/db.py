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
        _lodgesIds = query['lodges']
        _reservesAndOr = query['reservesAndOr']
        _reservesIds = query['reserves']
        _badgesAndOr = query['badgesAndOr']
        _badgesIds = query['badges']
        _animalsAndOr = query['animalsAndOr']
        _animalsIds = query['animals']

        def _getTables():
            if len(_lodgesIds) > 0 or len(_reservesIds) > 0 or len(_badgesIds) > 0 or len(_animalsIds) > 0:
                lodges = self._trophyAnimals.where(lodge=Table.is_in(_lodgesIds))
                reserves = self._trophyAnimals.where(reserve=Table.is_in(_reservesIds))
                badges = self._trophyAnimals.where(badge=Table.is_in(_badgesIds))
                animals = self._trophyAnimals.where(type=Table.is_in(_animalsIds))

                lodgesReserves = self._withAndOr(lodges, reserves, _reservesAndOr)
                lodgesReservesBadges = self._withAndOr(lodgesReserves, badges, _badgesAndOr)
                lodgesReservesBadgesAnimals = self._withAndOr(lodgesReservesBadges, animals, _animalsAndOr)
                return lodgesReservesBadgesAnimals
            return self._trophyAnimals

        return list(_getTables())


    def _withAndOr(self, first, second, andOr: str):
        if self._isAnd(andOr):
            return first.join(second, id="id")
        else:
            return first.outer_join(Table.FULL_OUTER_JOIN, second, id="id")


    @staticmethod
    def _isAnd(andOr):
        return andOr == 'and'

    def lodges(self) -> List[str]:
        return list(set(map(lambda a: a.lodge, self._trophyAnimals)))

