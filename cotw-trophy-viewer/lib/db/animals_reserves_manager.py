import sqlite3
from pathlib import Path
from typing import List

from lib.model.animalReserve import AnimalReserve


class AnimalsReservesManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
               CREATE TABLE IF NOT EXISTS AnimalsReserves (
                   reserve INTEGER,
                   type INTEGER,
                   PRIMARY KEY (reserve, type)
               )
           ''')
        conn.commit()
        conn.close()

    def insert_animals_reserves(self, animals_reserves: List[AnimalReserve]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM AnimalsReserves')
        for animal_reserve in animals_reserves:
            cursor.execute('''
                INSERT OR IGNORE INTO AnimalsReserves (reserve, type)
                VALUES (?, ?)
            ''', (animal_reserve.reserve.value, animal_reserve.type.value))
        conn.commit()
        conn.close()
