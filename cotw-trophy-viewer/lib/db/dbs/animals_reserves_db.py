import sqlite3
from pathlib import Path
from typing import List

from lib.model.animal_type_reserve import AnimalReserve


class AnimalReserveDb:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS AnimalsReserves')
        cursor.execute('''
               CREATE TABLE AnimalsReserves (
                   reserveId INTEGER,
                   typeId INTEGER,
                   PRIMARY KEY (reserveId, typeId)
               )
           ''')
        conn.commit()
        conn.close()

    def insert_animal_reserves(self, animals_reserves: List[AnimalReserve]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM AnimalsReserves')
        for animal_reserve in animals_reserves:
            cursor.execute('''
                INSERT OR IGNORE INTO AnimalsReserves (reserveId, typeId)
                VALUES (?, ?)
            ''', (animal_reserve.reserve.value, animal_reserve.type.value))
        conn.commit()
        conn.close()
