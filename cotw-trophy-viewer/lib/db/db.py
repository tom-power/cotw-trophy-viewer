import sqlite3 as sqlite
from typing import List

from lib.model.trophyanimal import TrophyAnimal


class Db:
    def __init__(self) -> None:
        self.conn = sqlite.connect('trophy_viewer.sqlite')

    def load(self, trophyAnimals: List[TrophyAnimal]):
        pass
