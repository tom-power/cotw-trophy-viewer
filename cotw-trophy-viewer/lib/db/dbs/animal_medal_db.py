import sqlite3
from pathlib import Path
from typing import List

from lib.model.animal_type_medal import AnimalMedal


class AnimalMedalDb:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS AnimalMedal')
        cursor.execute('''
               CREATE TABLE IF NOT EXISTS AnimalMedal (
                   medalId INTEGER,
                   typeId INTEGER,
                   PRIMARY KEY (medalId, typeId)
               )
           ''')
        conn.commit()
        conn.close()

    def insert_animal_medals(self, animals_medals: List[AnimalMedal]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM AnimalMedal')
        for animal_medal in animals_medals:
            cursor.execute('''
                INSERT OR IGNORE INTO AnimalMedal (medalId, typeId)
                VALUES (?, ?)
            ''', (animal_medal.medal.value, animal_medal.type.value))
        conn.commit()
        conn.close()
