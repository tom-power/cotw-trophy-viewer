import sqlite3
from pathlib import Path
from typing import List


class TrophyAnimalDb:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS TrophyAnimals  ')
        cursor.execute('''               
               CREATE TABLE TrophyAnimals (
                   typeId INTEGER,
                   weight REAL,
                   gender INTEGER,
                   rating REAL,
                   medalId REAL,
                   difficulty REAL,
                   datetime TEXT,
                   furType INTEGER,
                   lodgeId INTEGER,
                   lodgeType INTEGER,
                   lodgeTypeId INTEGER,
                   reserveId INTEGER
               )
           ''')

        conn.commit()
        conn.close()


    def insert_trophy_animals_dict(self, trophy_animals: List[dict]) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM TrophyAnimals')

        for animal in trophy_animals:
            cursor.execute('''
                INSERT INTO TrophyAnimals
                (typeId, weight, gender, rating, medalId, difficulty, datetime, furType, lodgeId, lodgeType, lodgeTypeId, reserveId)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                int(animal['typeId']) if animal['typeId'] is not None else None,
                float(animal['weight']) if animal['weight'] is not None else None,
                int(animal['gender']) if animal['gender'] is not None else None,
                float(animal['rating']) if animal['rating'] is not None else None,
                int(animal['medalId']) if animal['medalId'] is not None else None,
                float(animal['difficulty']) if animal['difficulty'] is not None else None,
                str(animal['datetime']),
                int(animal['furType']) if animal['furType'] is not None else None,
                int(animal['lodgeId']) if animal['lodgeId'] is not None else None,
                int(animal['lodgeType']) if animal['lodgeType'] is not None else None,
                int(animal['lodgeTypeId']) if animal['lodgeTypeId'] is not None else None,
                int(animal['reserveId']) if animal['reserveId'] is not None else None
            ))

        conn.commit()
        conn.close()
